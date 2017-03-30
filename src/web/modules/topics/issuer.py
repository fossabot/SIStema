import operator
import datetime

from django.db import transaction
from django.db.models import F
from django.utils import timezone
import django.core.mail

from . import models


class AlreadyIssuedException(Exception):
    pass


class NoMoreTopics(Exception):
    pass


class TopicIssuer:
    def __init__(self, user, questionnaire):
        self.user = user
        self.questionnaire = questionnaire

    @transaction.atomic
    def find_and_issue_new_topic_for_user(self):
        """
        :return: True if success, False if topics have finished
        """
        try:
            topic, scales = self.find_next_topic_to_issue()
        except NoMoreTopics:
            return False
        return self.issue_topic(topic, scales)

    @transaction.atomic
    def find_next_topic_to_issue(self):
        # Пользовательские оценки, выставленные в этой анкете, упорядоченные по
        # сложности вопроса
        user_marks = models.UserMark.objects.filter(
            user=self.user,
            scale_in_topic__topic__questionnaire=self.questionnaire
        ).order_by('scale_in_topic__topic__order')

        # Нулевые оценки пользователя
        zero_marks = user_marks.filter(mark=0)

        # Максимальные оценки пользователя
        max_marks = user_marks.filter(
            mark=F('scale_in_topic__scale_label_group__scale__count_values') - 1
        )

        # Ищем нулевую оценку на самую лёгкую тему (или просто самую сложную
        # тему, если нулевых оценок нет)
        ordered_topics = models.Topic.objects.filter(
            questionnaire=self.questionnaire).order_by('order')
        easiest_zero_mark = zero_marks.first()
        if easiest_zero_mark is None:
            easiest_unknown_topic = ordered_topics.last()
        else:
            easiest_unknown_topic = easiest_zero_mark.scale_in_topic.topic

        # и максимальную оценку на самую сложную тему (или просто самую лёгкую
        # тему)
        hardest_max_mark = max_marks.last()
        if hardest_max_mark is None:
            hardest_known_topic = ordered_topics.first()
        else:
            hardest_known_topic = hardest_max_mark.scale_in_topic.topic

        # Пытаемся найти некоторый средний уровень сложности
        middle_order = (easiest_unknown_topic.order +
                        hardest_known_topic.order) / 2
        # Мы потом отсортируем все шкалы, на которые мы ещё не знаем однозначный
        # ответ, относительно него, чтобы выбрать ближайшую к этому уровню шкалу
        # для выдачи пользователю

        # Вообще все шкалы во всех темах
        all_scales_topics = models.ScaleInTopic.objects.filter(
            topic__questionnaire=self.questionnaire).select_related('topic')
        # Шкалы в темах, на которые мы однозначно знаем оценку пользователя (от
        # него или автоматически посчитанную) (на самом деле их идентификаторы,
        # так как этого достаточно)
        scales_in_topics_with_ensured_answer = user_marks
        # not all database backends supports distinct
        # .distinct('scale_in_topic_id')

        scales_in_topics_with_ensured_answer = set(map(
            operator.attrgetter('scale_in_topic_id'),
            scales_in_topics_with_ensured_answer))

        # Шкалы, в оценках по которым мы не уверены
        scales_in_topics_with_no_ensured_answer = list(filter(
            lambda s: s.id not in scales_in_topics_with_ensured_answer,
            all_scales_topics))

        # Если таких нет, то заполнение тематической анкеты закончено
        if len(scales_in_topics_with_no_ensured_answer) == 0:
            raise NoMoreTopics()

        # Наконец-то находим шкалу в теме, оценки к которой мы не знаем и
        # которая располагается ближе всего к уровню сложности middle_order
        middle_unanswered_scale = min(
            scales_in_topics_with_no_ensured_answer,
            key=lambda s: abs(s.topic.order - middle_order))

        # Найдём все шкалы с неизвестной оценкой в той же теме, чтобы показать
        # их сразу
        middle_unanswered_topic = middle_unanswered_scale.topic
        middle_unanswered_topic_scales = list(filter(
            lambda s: s.topic == middle_unanswered_topic,
            scales_in_topics_with_no_ensured_answer))

        return middle_unanswered_topic, middle_unanswered_topic_scales

    @transaction.atomic
    def issue_topic(self, topic, scales_in_topic):
        if models.TopicIssue.objects.filter(
            user=self.user,
            topic=topic,
            created_at__lte=timezone.now() - datetime.timedelta(minutes=1)
        ).exists():
            all_marks = list(models.UserMark.objects.filter(
                user=self.user,
                scale_in_topic__topic__questionnaire=self.questionnaire
            ))
            message = ('{}: AlreadyIssuedException\n'
                       '  user_id = {}\n'
                       '  topic_id = {}\n'
                       '  all marks = {}\n'
                       ''.format(
                            datetime.datetime.now(),
                            self.user.id,
                            topic.id,
                            all_marks)
                        )
            print(message)
            django.core.mail.mail_admins('topics: AlreadyIssuedException', message)

        return self._internal_issue_topic(topic, scales_in_topic)

    def reissue_topic(self, topic, scales_in_topic):
        return self._internal_issue_topic(topic, scales_in_topic)

    @transaction.atomic
    def _internal_issue_topic(self, topic, scales_in_topic):
        topic_issue = models.TopicIssue(user=self.user, topic=topic)
        topic_issue.save()

        for scale_in_topic in scales_in_topic:
            if scale_in_topic.topic != topic:
                raise Exception('topics.issuer.TopicIssuer.issue_topic: scales '
                                'should point to the same topic')

            scale_in_topic_issue = models.ScaleInTopicIssue(
                topic_issue=topic_issue,
                label_group=scale_in_topic.scale_label_group)
            scale_in_topic_issue.save()

        return topic_issue

    def get_last_issued_topic(self):
        topic_issue = models.TopicIssue.objects.filter(
            topic__questionnaire=self.questionnaire, user=self.user
        ).order_by('-created_at').prefetch_related('scales').first()
        return topic_issue
