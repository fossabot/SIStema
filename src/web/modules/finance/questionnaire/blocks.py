import questionnaire.models

from .. import models


class PaymentInfoQuestionnaireBlock(questionnaire.models.MarkdownQuestionnaireBlock):
    block_name = 'payment_info'

    def fill_for_user(self, user):
        school = self.questionnaire.for_school
        if school is None:
            raise ValueError('modules.finance.questionnaire.PaymentInfoQuestionnaireBlock can be inserted only in school-related questionnaire')
        payment_amount = models.PaymentAmount.get_amount_for_user(school, user)

        if payment_amount is None:
            new_text = ''
        else:
            new_text = self.markdown.replace('{{ payment_amount }}', str(payment_amount))
        return questionnaire.models.MarkdownQuestionnaireBlock(markdown=new_text)
