from modules.entrance import steps
from .. import models


class PaymentInfoEntranceStep(steps.EntranceStep):
    def __init__(self, school, payment_questionnaire, previous_questionnaire=None):
        super().__init__(school, previous_questionnaire=previous_questionnaire)
        self.payment_questionnaire = payment_questionnaire
        if self.payment_questionnaire.for_school_id != self.school.id:
            raise ValueError('topics.entrance.steps.TopicQuestionnaireEntranceStep: Questionnaire must be for this school')

    def is_passed(self, user):
        return self.payment_questionnaire.is_filled_by(user) and super().is_passed(user)

    def render(self, user):
        if not self.is_available(user):
            template = self._template_factory('''
            <p>
                {{ questionnaire.title }} будет доступна после заполнения раздела «{{ previous.title }}».
            </p>
            ''')
            body = template.render({
                'questionnaire': self.payment_questionnaire,
                'previous': self.previous_questionnaire,
            })
            return self.panel(self.payment_questionnaire.title, body, 'default')

        payment_amount = models.PaymentAmount.get_amount_for_user(self.school, user)

        user_discounts = models.Discount.objects.filter(for_school=self.school, for_user=user)
        actual_discounts = user_discounts.filter(amount__gt=0)
        considered_discounts = user_discounts.filter(amount=0)

        template = self._template_factory('''
            {% load stringcase %}

            {% if payment_amount %}
                <p>
                    Размер оргвзноса для вас с учётом скидок составляет <b>{{ payment_amount }} рублей</b>.
                </p>
                <p>
                    {% if actual_discounts %}
                        <b>Предоставленн{{ actual_discounts.count|pluralize:'ая,ые' }} скидк{{ actual_discounts.count|pluralize:'а,и' }}: </b>
                        {% for discount in actual_discounts %}
                            {% if discount.public_comment %}
                                {{ discount.public_comment }}
                            {% else %}
                                {{ discount.type_name|lowerfirst }}
                            {% endif %}
                            в размере {{ discount.amount }} рублей{% if not forloop.last %},{% endif %}
                        {% endfor %}
                    {% endif %}

                    {% if considered_discounts %}
                        Вы <b>рассматриваетесь</b> на получение скид{{ considered_discounts.count|pluralize:'ки,ок' }}:
                        {% for discount in considered_discounts %}
                            {% if discount.public_comment %}
                                {{ discount.public_comment }}
                            {% else %}
                                {{ discount.type_name }}
                            {% endif %}
                            {% if not forloop.last %},{% endif %}
                        {% endfor %}
                    {% endif %}
                </p>
            {% endif %}
            <p>
                Заполните информацию об оплате до <b>20 июня</b>.
            </p>
            <div>
                <a class="btn btn-alert" href="{{ questionnaire.get_absolute_url }}">Заполнить</a>
            </div>
            ''')
        body = template.render({
            'user': user,
            'school': self.school,
            'questionnaire': self.payment_questionnaire,
            'payment_amount': payment_amount,
            'actual_discounts': actual_discounts,
            'considered_discounts': considered_discounts,
        })

        return self.panel(self.payment_questionnaire.title, body, 'alert')

