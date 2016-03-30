from django.contrib import admin

from . import models

admin.site.register(models.Questionnaire)
admin.site.register(models.ChoiceQuestionnaireQuestion)
admin.site.register(models.ChoiceQuestionnaireQuestionVariant)
admin.site.register(models.TextQuestionnaireQuestion)
admin.site.register(models.YesNoQuestionnaireQuestion)

admin.site.register(models.UserQuestionnaireStatus)
admin.site.register(models.QuestionnaireAnswer)
