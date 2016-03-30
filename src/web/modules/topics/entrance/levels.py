import collections
import operator

from modules.entrance import levels
from modules.entrance import models as entrance_models
from .. import settings
from .. import models

from django.db import models as django_models


# TODO: move to models.py?
class EntranceLevelRequirement(django_models.Model):
    """
    Каждое требование задаётся кортежом (tag, max_penalty).
    Это значит, что сумма баллов школьника по всем шкалам всех тем с тегом tag должна отличаться
    от максимальной не более чем на max_penalty.
    """
    questionnaire = django_models.ForeignKey(models.TopicQuestionnaire)

    entrance_level = django_models.ForeignKey(entrance_models.EntranceLevel)

    tag = django_models.ForeignKey(settings.Tag)

    max_penalty = django_models.PositiveIntegerField()

    class Meta:
        unique_together = ('questionnaire', 'entrance_level', 'tag')

    def satisfy(self, sum_marks, max_marks):
        return max_marks - sum_marks <= self.max_penalty


# TODO: move to helpers
def group_by(objects_list, func):
    result = collections.defaultdict(list)
    for obj in objects_list:
        result[func(obj)].append(obj)
    return result


# TODO: cache results for each users
class TopicsEntranceLevelLimiter(levels.EntranceLevelLimiter):
    def __init__(self, school):
        super().__init__(school)
        self.questionnaire = self.school.topicquestionnaire
        if self.questionnaire is None:
            raise Exception('modules.topics.entrance.levels.TopicsEntranceLevelLimiter:'
                            'can\'t use TopicsEntranceLevelLimiter without topics questionnaire for this school')

    def get_limit(self, user):
        # TODO: check status, if not FINISHED, return self._find_minimal_level()

        user_marks = models.UserMark.objects.filter(user=user, scale_in_topic__topic__questionnaire=self.questionnaire)\
            .prefetch_related('scale_in_topic__topic__tags')

        requirements = list(EntranceLevelRequirement.objects.filter(questionnaire=self.questionnaire)
                            .prefetch_related('entrance_level'))
        requirements_by_tag = group_by(requirements, operator.attrgetter('tag_id'))
        requirements_by_level = group_by(requirements, operator.attrgetter('entrance_level'))
        sum_marks_for_requirements = collections.defaultdict(int)
        max_marks_for_requirements = collections.defaultdict(int)

        for mark in user_marks:
            scale_in_topic = mark.scale_in_topic
            topic = scale_in_topic.topic
            topic_tags = topic.tags.all()

            for tag in topic_tags:
                for requirement in requirements_by_tag[tag.id]:
                    sum_marks_for_requirements[requirement.id] += mark.mark
                    max_marks_for_requirements[requirement.id] += scale_in_topic.scale.max_mark

        # Даже если всё идеально, самый сложный уровень считаем невыполненным — иначе нечего будет решать
        minimum_non_satisfied_level = entrance_models.EntranceLevel.objects.filter(for_school=self.school)\
            .order_by('order').last()
        for level, requirements_for_level in requirements_by_level.items():
            all_satisfied = True
            for requirement in requirements_for_level:
                all_satisfied = all_satisfied and requirement.satisfy(sum_marks_for_requirements[requirement.id],
                                                                      max_marks_for_requirements[requirement.id])

            if not all_satisfied:
                if level.order < minimum_non_satisfied_level.order:
                    minimum_non_satisfied_level = level

        return levels.EntranceLevelLimit(minimum_non_satisfied_level)