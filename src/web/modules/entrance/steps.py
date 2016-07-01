from django.template import engines, Context
from django.utils.safestring import mark_safe


class EntranceStep:
    # TODO: replace previous_questionnaire to previous_step
    def __init__(self, school, previous_questionnaire=None):
        self.school = school
        self._template_factory = engines['django'].from_string

        self.previous_questionnaire = previous_questionnaire
        if self.previous_questionnaire is not None \
                and self.previous_questionnaire.for_school is not None \
                and self.previous_questionnaire.for_school_id != self.school.id:
            raise ValueError('entrance.steps.EntranceStep: Previous questionnaire must be for this school')

    def is_passed(self, user):
        return True

    def is_available(self, user):
        if self.previous_questionnaire is None:
            return True
        return self.previous_questionnaire.is_filled_by(user)

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
            'panel_body': mark_safe(panel_body),
            'panel_color': panel_color
        }))


class QuestionnaireEntranceStep(EntranceStep):
    def __init__(self, school, questionnaire, previous_questionnaire=None, message=None, closed_message=None, button_text=None):
        super().__init__(school, previous_questionnaire=previous_questionnaire)

        self.questionnaire = questionnaire
        if self.questionnaire.for_school is not None and self.questionnaire.for_school_id != self.school.id:
            raise ValueError('entrance.steps.QuestionnaireEntranceStep: Questionnaire must be for this school')

        self.message = message
        if self.message is None:
            self.message = '{{ user.first_name }}, чтобы подать заявку в {{ school.name }} нужно заполнить информацию о себе'

        self.closed_message = closed_message
        if self.closed_message is None:
            self.closed_message = 'Вступительная работа завершена. Вы не можете вносить изменения в анкету, но можете её посмотреть.'

        self.button_text = button_text
        if self.button_text is None:
            self.button_text = 'Заполнить'

    def is_passed(self, user):
        return self.questionnaire.is_filled_by(user) and super().is_passed(user)

    def is_available(self, user):
        return super().is_available(user)

    def render(self, user):
        if self.is_available(user) and self.questionnaire.is_closed():
            template = self._template_factory('''
            <p>
                {{ closed_message }}
            </p>
            <div>
                <a class="btn btn-default" href="{{ questionnaire.get_absolute_url }}">Посмотреть</a>
            </div>
            ''')
            body = template.render(Context({
                'questionnaire': self.questionnaire,
                'closed_message': self.closed_message,
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
                Раздел «{{ questionnaire.title }}» заполнен. Вы можете изменить что-нибудь, если хотите.
            </p>
            <div>
                <a class="btn btn-success" href="{{ questionnaire.get_absolute_url }}">Править</a>
            </div>
            ''')
            body = template.render(Context({
                'user': user,
                'questionnaire': self.questionnaire,
            }))

            return self.panel(self.questionnaire.title, body, 'success')

        template = self._template_factory('''
        <p>
            ''' + self.message + '''.
        </p>
        <div>
            <a class="btn btn-alert" href="{{ questionnaire.get_absolute_url }}">{{ button_text }}</a>
        </div>
        ''')
        body = template.render(Context({
            'user': user,
            'school': self.school,
            'questionnaire': self.questionnaire,
            'button_text': self.button_text
        }))

        return self.panel(self.questionnaire.title, body, 'alert')


class ExamEntranceStep(EntranceStep):
    def __init__(self, school, previous_questionnaire=None):
        super().__init__(school, previous_questionnaire=previous_questionnaire)
        self.exam = self.school.entranceexam
        if self.exam is None:
            raise ValueError('entrance.steps.ExamEntranceStep: School must have defined entrance exam for this step')

    def is_passed(self, user):
        return super().is_passed(user)

    def is_available(self, user):
        return super().is_available(user)

    def render(self, user):
        if self.is_available(user) and self.exam.is_closed():
            template = self._template_factory('''
            <p>
                Вступительная работа завершена. Вы не можете отправлять новые решения.
            </p>
            <div>
                <a class="btn btn-default" href="{{ exam.get_absolute_url }}">Посмотреть отправленные решения</a>
            </div>
            ''')
            body = template.render(Context({
                'exam': self.exam,
            }))
            return self.panel('Вступительная работа', body, 'default')

        if not self.is_available(user):
            template = self._template_factory('''
            <p>
                Задания будут доступны после заполнения раздела «{{ previous.title }}».
            </p>
            ''')
            body = template.render(Context({
                'exam': self.exam,
                'previous': self.previous_questionnaire,
            }))
            return self.panel('Вступительная работа', body, 'default')

        template = self._template_factory('''
        <p>
            И наконец-то вступительная работа. На основе тематической анкеты мы отобрали для вас задачи, попробуйте!
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
