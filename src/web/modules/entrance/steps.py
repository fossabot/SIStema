from django.template import engines, Context


class EntranceStep:
    def __init__(self, school):
        self.school = school
        self._template_factory = engines['django'].from_string

    def is_available(self, user):
        raise NotImplementedError('Child should implement its own is_available()')

    def is_passed(self, user):
        raise NotImplementedError('Child should implement its own is_passed()')

    def render(self, user):
        raise NotImplementedError('Child should implement its own render()')

    def panel(self, panel_title, panel_body, panel_color='default'):
        template = self._template_factory('''
        <div class="admin-form">
            <div class="panel panel-{{ panel_color }} heading-border">
                <div class="panel-heading">
                    <span class="panel-title">
                        {{ panel_title }}
                    </span>
                </div>

                <div class="panel-body">
                    {{ panel_body }}
                </div>
            </div>
        </div>
        ''')
        return template.render(Context({
            'panel_title': panel_title,
            'panel_body': panel_body,
            'panel_color': panel_color
        }))


class QuestionnaireEntranceStep(EntranceStep):
    def __init__(self, school, questionnaire):
        super(QuestionnaireEntranceStep, self).__init__(school)
        self.questionnaire = questionnaire
        if self.questionnaire.for_school is not None and self.questionnaire.for_school_id != self.school.id:
            raise ValueError('entrance.steps.QuestionnaireEntranceStep: Questionnaire must be for this school')

    def is_passed(self, user):
        return False

    def is_available(self, user):
        return True

    def render(self, user):
        template = self._template_factory('''
        <p>
            {{ user.first_name }}, чтобы подать заявку в {{ school.name }} нужно заполнить информацию о себе.
        </p>
        <div>
            <a class="btn btn-alert" href="{{ questionnaire.get_absolute_url }}">Подать заявку</a>
        </div>
        ''')
        body = template.render(Context({
            'user': user,
            'school': self.school,
            'questionnaire': self.questionnaire,
        }))

        return self.panel(self.questionnaire.title, body, 'alert')


class ExamEntranceStep(EntranceStep):
    def __init__(self, school):
        super(ExamEntranceStep, self).__init__(school)
        self.exam = self.school.entranceexam
        if self.exam is None:
            raise ValueError('entrance.steps.ExamEntranceStep: School must have defined entrance exam for this step')

    def is_passed(self, user):
        pass

    def is_available(self, user):
        pass

    def render(self, user):
        template = self._template_factory('''
        <p>
            И наконец-то вступительная работа. На основе тематическоя анкеты мы отобрали для вас задачи, попробуйте!
        </p>
        <div>
            <a class="btn btn-alert" href="{{ exam.get_absolute_url }}">Решать</a>
        </div>
        ''')
        body = template.render(Context({
            'user': user,
            'school': self.school,
            'exam': self.exam,
        }))

        return self.panel('Вступительная работа', body, 'alert')
