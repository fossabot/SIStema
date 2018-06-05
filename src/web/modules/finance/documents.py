from . import models
import generator.models
import schools.models
import questionnaire.models
from modules.entrance.models import EntranceStatus
from generator import generator
import datetime

class DocumentGenerator:
    def __init__(self, school):
        self.school = school
        self.payment_questionnaire = questionnaire.models.Questionnaire.objects.filter(
            school=self.school,
            short_name='payment'
        ).first()

        # TODO (andgein): This code should not contain questionnaire short_name
        if self.payment_questionnaire is None:
            self.payment_questionnaire = questionnaire.models.Questionnaire.objects.filter(
                school=self.school,
                short_name__in=['parent', 'details']
            ).first()

        # For invitations to foreign countries
        self.visa_questionnaire = questionnaire.models.Questionnaire.objects.filter(
            school=self.school,
            short_name='august_passport_visa'
        ).first()
        
        self.questions = {
            'payment': self._get_questions(self.payment_questionnaire),
            'visa': self._get_questions(self.visa_questionnaire),
        }

    
    def _get_questions(self, current_questionnaire):
        questions = questionnaire.models.AbstractQuestionnaireQuestion.objects.filter(
            questionnaire=current_questionnaire
        )
        questions = {q.short_name: q for q in questions}

        questionnaire_choice_variants = list(
            questionnaire.models.ChoiceQuestionnaireQuestionVariant.objects.filter(
                question__questionnaire=current_questionnaire
            )
        )
        questionnaire_choice_variants = {v.id: v for v in questionnaire_choice_variants}

        return {
            'questions': questions,
            'choices': questionnaire_choice_variants,
        }


    # Return just user's answer if it's a text, integer or date,
    # otherwise return corresponding option from ChoiceQuestionnaireQuestionVariant
    def _get_question_answer(self, user_answer, questions):
        question_short_name = user_answer.question_short_name
        question = questions['questions'][question_short_name]

        if user_answer.answer.strip() == '':
            return ''

        if isinstance(question, questionnaire.models.ChoiceQuestionnaireQuestion):
            return questions['choices'][int(user_answer.answer)].text

        return user_answer.answer


    def _get_dict_questionnaire(self, user, current_questionnaire, questions):
        user_questionnaire = list(
            questionnaire.models.QuestionnaireAnswer.objects.filter(
                questionnaire=current_questionnaire,
                user=user
            )
        )
        user_questionnaire = {
            a.question_short_name: self._get_question_answer(a, questions)
            for a in user_questionnaire
        }
        return user_questionnaire


    def generate(self, document_type, user):
        # if not self.payment_questionnaire.is_filled_by(user):
        #     raise ValueError('User has not fill the payment questionnaire')
        user_payment_questionnaire = self._get_dict_questionnaire(user, self.payment_questionnaire, self.questions['payment'])
        user_visa_questionnaire = self._get_dict_questionnaire(user, self.visa_questionnaire, self.questions['visa'])

        entrance_status = EntranceStatus.get_visible_status(self.school, user)
        if entrance_status is None or entrance_status.status != EntranceStatus.Status.ENROLLED:
            raise ValueError('User has not enrolled')

        session_and_parallel = entrance_status.sessions_and_parallels.filter(selected_by_user=True).first()
        if session_and_parallel is None:
            raise ValueError('User did not select session for him')
        session = session_and_parallel.session

        price = models.PaymentAmount.get_amount_for_user(self.school, user)

        g = generator.TemplateGenerator(document_type.template)
        return g.generate({
            'school': self.school,
            'session': session,
            'student': user.profile,
            'contract': {
                'id': user.id,
                'created_at': datetime.date.today()
            },
            'payment': user_payment_questionnaire,
            'price': price,
            'visa' : user_visa_questionnaire,
        })
