from django.contrib import admin

from . import models


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'short_name',
        'title',
        'for_school',
        'for_session',
    )

admin.site.register(models.Questionnaire, QuestionnaireAdmin)


class AbstractQuestionnaireQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'short_name',
        'is_required',
        'questionnaire',
        'order',
    )

    list_filter = ('questionnaire', 'is_required')
    ordering = ('order',)

admin.site.register(models.ChoiceQuestionnaireQuestion, AbstractQuestionnaireQuestionAdmin)
admin.site.register(models.TextQuestionnaireQuestion, AbstractQuestionnaireQuestionAdmin)
admin.site.register(models.YesNoQuestionnaireQuestion, AbstractQuestionnaireQuestionAdmin)


class ChoiceQuestionnaireQuestionVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text')
    list_filter = ('question',)

admin.site.register(models.ChoiceQuestionnaireQuestionVariant,
                    ChoiceQuestionnaireQuestionVariantAdmin)


class UserQuestionnaireStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'questionnaire', 'status')
    list_filter = ('questionnaire', 'status')
    search_fields = (
        '=user__username',
        '=user__email',
        '=user__first_name',
        '=user__last_name',
    )

admin.site.register(models.UserQuestionnaireStatus, UserQuestionnaireStatusAdmin)


class QuestionnaireAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'questionnaire', 'question_short_name', 'answer')
    list_filter = ('questionnaire',)
    search_fields = (
        '=user__username',
        '=user__email',
        '=user__first_name',
        '=user__last_name',
    )

admin.site.register(models.QuestionnaireAnswer, QuestionnaireAnswerAdmin)
