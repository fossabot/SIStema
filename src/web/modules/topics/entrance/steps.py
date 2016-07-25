from modules.entrance import steps
from .. import models

from django.template import Context


class TopicQuestionnaireEntranceStep(steps.EntranceStep):
    def __init__(self, school, questionnaire, previous_questionnaire=None):
        super().__init__(school, previous_questionnaire=previous_questionnaire)
        self.questionnaire = questionnaire
        if self.questionnaire.school_id != self.school.id:
            raise ValueError('topics.entrance.steps.TopicQuestionnaireEntranceStep: Questionnaire must be for this school')

    def is_passed(self, user):
        return self.questionnaire.is_filled_by(user) and super().is_passed(user)

    def is_available(self, user):
        return super().is_available(user)

    def render(self, user):
        if self.is_available(user) and self.questionnaire.is_closed():
            template = self._template_factory('''
            <p>
                Вступительная работа завершена.
            </p>
            <div>
                <a class="btn btn-default" href="{{ questionnaire.get_absolute_url }}">Посмотреть анкету</a>
            </div>
            ''')
            body = template.render(Context({
                'questionnaire': self.questionnaire,
            }))

            return self.panel(self.questionnaire.title, body, 'default')

        if not self.is_available(user):
            template = self._template_factory('''
            <p>
                {{ questionnaire.title }} будет доступна после заполнения раздела «{{ previous.title }}».
            </p>
            ''')
            body = template.render(Context({
                'questionnaire': self.questionnaire,
                'previous': self.previous_questionnaire,
            }))
            return self.panel(self.questionnaire.title, body, 'default')

        if self.is_passed(user):
            template = self._template_factory('''
            <p>
                {{ questionnaire.title }} заполнена. Вносить изменения запрещено. На основе анкеты вам выданы задачи
                во вступительной работе. Удачи!
            </p>
            <p>
                Если вы <strong>освобождены</strong> от выполнения вступительной работы, на этом можно остановиться.
            </p>
            <p>
                Вступительная работа в параллель P опубликована на
                <a href="https://lksh.ru/sis/2016/parallel-p.shtml">сайте</a>.
            </p>
            <div>
                <a class="btn btn-success" href="{{ questionnaire.get_absolute_url }}">Посмотреть</a>
            </div>
            ''')
            body = template.render(Context({
                'user': user,
                'questionnaire': self.questionnaire,
            }))

            return self.panel(self.questionnaire.title, body, 'success')

        if self.questionnaire.get_status(user) == models.UserQuestionnaireStatus.Status.STARTED:
            template = self._template_factory('''
            <p>
                Вы не закончили заполнять тематическую анкету.
            </p>

            <p>
                <span class="fa fa-warning"></span>
                Заполните её, даже если вы освобождены от выполнения вступительной работы.
            </p>
            <div>
                <a class="btn btn-danger pastel" href="{{ questionnaire.get_absolute_url }}">Продолжить</a>
            </div>
            ''')
            body = template.render(Context({
                'user': user,
                'questionnaire': self.questionnaire,
            }))

            return self.panel(self.questionnaire.title, body, 'danger pastel')

        if self.questionnaire.get_status(user) == models.UserQuestionnaireStatus.Status.CORRECTING:
            template = self._template_factory('''
            <p>
                Вы не проверили правильность оценок тематической анкеты.
            </p>
            <p>
                Это можно сделать в любой момент,
                но без этого вы не сможете получить задачи вступительной работы.
            </p>

            <div>
                <a class="btn btn-danger pastel" href="{{ questionnaire.get_absolute_url }}">Проверить оценки</a>
            </div>
            ''')
            body = template.render(Context({
                'user': user,
                'questionnaire': self.questionnaire,
            }))

            return self.panel(self.questionnaire.title, body, 'danger pastel')

        template = self._template_factory('''
        <p>
            Тематическая анкета &mdash; важная составляющая поступления в ЛКШ. После её заполнения
            вам будут выданы задания вступительной работы, которые будет необходимо решить.
        </p>
        <p>
            <span class="fa fa-warning"></span>
            Заполните её, даже вы освобождены от выполнения вступительной работы.
        </p>
        <div>
            <a class="btn btn-alert" href="{{ questionnaire.get_absolute_url }}">Заполнить</a>
        </div>
        ''')
        body = template.render(Context({
            'user': user,
            'school': self.school,
            'questionnaire': self.questionnaire
        }))

        return self.panel(self.questionnaire.title, body, 'alert')
