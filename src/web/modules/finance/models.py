from django.db import models
import django.db.migrations.writer
from django.conf import settings

import djchoices
import polymorphic.models
import relativefilepathfield.fields
from cached_property import cached_property

from .questionnaire.blocks import PaymentInfoQuestionnaireBlock
import school.models
import user.models
import questionnaire.models
import generator.models


class Discount(models.Model):
    class Type(djchoices.DjangoChoices):
        SOCIAL = djchoices.ChoiceItem(1, 'Социальная скидка')
        PARTNER = djchoices.ChoiceItem(2, 'Скидка от партнёра')
        STATE = djchoices.ChoiceItem(3, 'Скидка от государства')
        OLYMPIADS = djchoices.ChoiceItem(4, 'Олимпиадная скидка')

    for_school = models.ForeignKey(school.models.School, related_name='+')

    for_user = models.ForeignKey(user.models.User, related_name='discounts')

    type = models.PositiveIntegerField(choices=Type.choices, validators=[Type.validator])

    # If amount = 0, discount is considered now
    amount = models.PositiveIntegerField(help_text='Размер скидки. Выберите ноль, чтобы скидка считалась «рассматриваемой»')

    private_comment = models.TextField(blank=True, help_text='Не показывается школьнику')

    public_comment = models.TextField(blank=True, help_text='Показывается школьнику')

    @property
    def type_name(self):
        return self.Type.values[self.type]


class PaymentAmount(models.Model):
    for_school = models.ForeignKey(school.models.School, related_name='+')

    for_user = models.ForeignKey(user.models.User, related_name='+')

    amount = models.PositiveIntegerField(help_text='Сумма к оплате')

    class Meta:
        unique_together = ('for_school', 'for_user')

    @classmethod
    def get_amount_for_user(cls, school, user):
        amount = cls.objects.filter(for_school=school, for_user=user).first()
        if amount is None:
            return None
        amount = amount.amount

        discounts = Discount.objects.filter(for_school=school, for_user=user).values_list('amount', flat=True)
        max_discount = max(discounts, default=0)

        amount -= max_discount
        if amount < 0:
            amount = 0

        return amount


class DocumentType(models.Model):
    short_name = models.CharField(max_length=100,
                                  help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием')

    for_school = models.ForeignKey(school.models.School)

    name = models.TextField()

    additional_information = models.TextField(
        help_text='Показывается школьнику перед скачиванием.'
                  'Например, «Распечатайте его в двух экземплярах, подпишите со своей стороны и привезите в ЛКШ»',
        blank=True, default='')

    template = models.ForeignKey(generator.models.Document, related_name='+')

    class Meta:
        unique_together = ('for_school', 'short_name')

    def __str__(self):
        return self.name

    # Document is need for user if there is no generation conditions for it
    # or if it is satisfied at least one of them
    def is_need_for_user(self, user):
        conditions = self.generation_conditions.all()
        if len(conditions) == 0:
            return True

        for condition in conditions:
            if condition.is_satisfied(user):
                return True

        return False


class Document(models.Model):
    for_school = models.ForeignKey(school.models.School)

    for_users = models.ManyToManyField(user.models.User)

    type = models.ForeignKey(DocumentType, related_name='generated_documents')

    filename = relativefilepathfield.fields.RelativeFilePathField(
        path=django.db.migrations.writer.SettingsReference(
            settings.SISTEMA_FINANCE_DOCUMENTS,
            'SISTEMA_FINANCE_DOCUMENTS'
        ),
        recursive=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def _users_list(self):
        return ', '.join(str(u) for u in self.for_users)


class AbstractDocumentGenerationCondition(polymorphic.models.PolymorphicModel):
    document_type = models.ForeignKey(DocumentType, related_name='generation_conditions')

    def is_satisfied(self, user):
        raise NotImplementedError('Child should implement its own is_satisfied()')


class QuestionnaireVariantDocumentGenerationCondition(AbstractDocumentGenerationCondition):
    variant = models.ForeignKey(questionnaire.models.ChoiceQuestionnaireQuestionVariant, related_name='+')

    @cached_property
    def question(self):
        return self.variant.question

    def is_satisfied(self, user):
        qs = questionnaire.models.QuestionnaireAnswer.objects.filter(
            questionnaire_id=self.question.questionnaire_id,
            question_short_name=self.question.short_name,
            for_user=user,
            answer=self.variant.id
        )
        return qs.exists()
