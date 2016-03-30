from django.contrib import admin

from . import models
from .entrance import levels


admin.site.register(models.TopicQuestionnaire)
admin.site.register(models.Topic)
admin.site.register(models.TopicDependency)
admin.site.register(models.Level)
admin.site.register(models.LevelDownwardDependency)
admin.site.register(models.LevelUpwardDependency)
admin.site.register(models.Scale)
admin.site.register(models.ScaleLabelGroup)
admin.site.register(models.ScaleLabel)
admin.site.register(models.ScaleInTopic)
admin.site.register(models.Tag)

admin.site.register(models.UserQuestionnaireStatus)
admin.site.register(models.UserMark)
admin.site.register(models.TopicIssue)
admin.site.register(models.ScaleInTopicIssue)

admin.site.register(levels.EntranceLevelRequirement)
