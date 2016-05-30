from django.db import models
import django.db.migrations.writer
from django.conf import settings

from cached_property import cached_property
import relativefilepathfield.fields
import polymorphic.models

import school.models
import generator.models
import user.models
import questionnaire.models


__all__ = ['DocumentType',
           'Document',
           'AbstractDocumentGenerationCondition',
           'QuestionnaireVariantDocumentGenerationCondition'
           ]


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
            user=user,
            answer=self.variant.id
        )
        return qs.exists()
