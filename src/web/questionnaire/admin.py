from django.contrib import admin
from polymorphic.admin import (PolymorphicChildModelAdmin,
                               PolymorphicChildModelFilter)

import sistema.polymorphic
from . import models

import groups.admin

@admin.register(models.Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'title', 'school', 'session')


@admin.register(models.AbstractQuestionnaireBlock)
class AbstractQuestionnaireBlockAdmin(
        sistema.polymorphic.PolymorphicParentModelAdmin
):
    base_model = models.AbstractQuestionnaireBlock
    list_display = (
        'id',
        'questionnaire',
        'short_name',
        'order',
    )
    list_filter = ('questionnaire', PolymorphicChildModelFilter)
    ordering = ('questionnaire', 'order')


class QuestionnaireBlockShowConditionInline(admin.StackedInline):
    model = models.QuestionnaireBlockShowCondition
    extra = 1


@admin.register(models.AbstractQuestionnaireQuestion)
@admin.register(models.MarkdownQuestionnaireBlock)
@admin.register(models.TextQuestionnaireQuestion)
@admin.register(models.YesNoQuestionnaireQuestion)
@admin.register(models.DateQuestionnaireQuestion)
class AbstractQuestionnaireBlockChildAdmin(PolymorphicChildModelAdmin):
    base_model = models.AbstractQuestionnaireBlock
    inlines = (QuestionnaireBlockShowConditionInline,)


class ChoiceQuestionnaireQuestionVariantInline(admin.TabularInline):
    model = models.ChoiceQuestionnaireQuestionVariant
    extra = 1
    ordering = ('order',)


@admin.register(models.ChoiceQuestionnaireQuestion)
class ChoiceQuestionnaireQuestionQuestionChildAdmin(PolymorphicChildModelAdmin):
    base_model = models.AbstractQuestionnaireBlock
    inlines = (QuestionnaireBlockShowConditionInline,
               ChoiceQuestionnaireQuestionVariantInline,)


@admin.register(models.ChoiceQuestionnaireQuestionVariant)
class ChoiceQuestionnaireQuestionVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text')
    list_filter = ('question',)


@admin.register(models.UserQuestionnaireStatus)
class UserQuestionnaireStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'questionnaire', 'status')
    list_filter = ('questionnaire', 'status')
    search_fields = (
        '=user__username',
        '=user__email',
        '=user__first_name',
        '=user__last_name',
        'user__profile__first_name',
        'user__profile__last_name',
    )


@admin.register(models.QuestionnaireAnswer)
class QuestionnaireAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'questionnaire',
        'question_short_name',
        'answer',
    )
    list_filter = ('questionnaire',)
    search_fields = (
        '=user__username',
        '=user__email',
        '=user__first_name',
        '=user__last_name',
        'user__profile__first_name',
        'user__profile__last_name',
    )


@admin.register(models.QuestionnaireBlockShowCondition)
class QuestionnaireBlockShowConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'block', 'need_to_be_checked')
    list_filter = ('block__questionnaire',)


@admin.register(models.UsersFilledQuestionnaireGroup)
@admin.register(models.UsersNotFilledQuestionnaireGroup)
class QuestionnaireGroupAdmin(groups.admin.AbstractGroupAdmin):
    pass
