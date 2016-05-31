from django.db import models

import school.models
import user.models
import questionnaire.models

import polymorphic.models


class EnrolledScanRequirement(models.Model):
    for_school = models.ForeignKey(school.models.School)

    short_name = models.CharField(max_length=100, help_text='Используется в урлах. Лучше обойтись маленькими буквами, цифрами и подчёркиванием')

    name = models.TextField(help_text='Например, «Квитанция об оплате»')

    name_genitive = models.TextField(help_text='Например, «квитанцию об оплате»')

    def __str__(self):
        return '%s. Скан «%s»' % (self.for_school, self.name)

    class Meta:
        unique_together = ('for_school', 'short_name')

    # ScanRequirement is needed for user if there is no conditions for it
    # or if this user is satisfied at least one of them
    def is_needed_for_user(self, user):
        conditions = self.conditions.all()
        if len(conditions) == 0:
            return True

        return any(c.is_satisfied(user) for c in conditions)


class EnrolledScan(models.Model):
    requirement = models.ForeignKey(EnrolledScanRequirement)

    for_user = models.ForeignKey(user.models.User)

    original_filename = models.TextField()

    filename = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )


class EnrolledScanRequirementCondition(polymorphic.models.PolymorphicModel):
    requirement = models.ForeignKey(EnrolledScanRequirement, related_name='conditions')

    def is_satisfied(self, user):
        raise NotImplementedError('Child should implement its own is_satisfied()')


class QuestionnaireVariantEnrolledScanRequirementCondition(EnrolledScanRequirementCondition):
    variant = models.ForeignKey(questionnaire.models.ChoiceQuestionnaireQuestionVariant,
                                related_name='+',
                                help_text='Вариант, который должен быть отмечен')

    def is_satisfied(self, user):
        return questionnaire.models.QuestionnaireAnswer.objects.filter(
            questionnaire=self.variant.question.questionnaire,
            question_short_name=self.variant.question.short_name,
            user=user,
            answer=self.variant.id
        ).exists()
