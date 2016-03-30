from modules.entrance import steps

from django.template import Context


class TopicQuestionnaireEntranceStep(steps.EntranceStep):
    def __init__(self, school, questionnaire):
        super().__init__(school)
        self.questionnaire = questionnaire
        if self.questionnaire.for_school_id != self.school.id:
            raise ValueError('topics.entrance.steps.TopicQuestionnaireEntranceStep: Questionnaire must be for this school')

    def is_passed(self, user):
        return False

    def is_available(self, user):
        return True

    def render(self, user):
        template = self._template_factory('''
        <p>
            Тематическая анкета &mdash; важная составляющая поступления в ЛКШ. После её заполнения
            вам будут выданы задания вступительной работы, которые будет необходимо решить.
        </p>
        <div>
            <a class="btn btn-alert" href="{{ questionnaire.get_absolute_url }}">Перейти к заполнению</a>
        </div>
        ''')
        body = template.render(Context({
            'user': user,
            'school': self.school,
            'questionnaire': self.questionnaire
        }))

        return self.panel(self.questionnaire.title, body, 'alert')
