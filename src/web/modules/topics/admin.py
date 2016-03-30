from django.contrib import admin

from . import settings
from . import models
from .entrance import levels


admin.site.register(settings.TopicQuestionnaire)
admin.site.register(settings.Topic)
admin.site.register(settings.TopicDependency)
admin.site.register(settings.Level)
admin.site.register(settings.LevelDownwardDependency)
admin.site.register(settings.LevelUpwardDependency)
admin.site.register(settings.Scale)
admin.site.register(settings.ScaleLabelGroup)
admin.site.register(settings.ScaleLabel)
admin.site.register(settings.ScaleInTopic)
admin.site.register(settings.Tag)

admin.site.register(models.UserQuestionnaireStatus)
admin.site.register(models.UserMark)
admin.site.register(models.TopicIssue)
admin.site.register(models.ScaleInTopicIssue)

admin.site.register(levels.EntranceLevelRequirement)
