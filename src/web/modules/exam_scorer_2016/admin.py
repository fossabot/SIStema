from django.contrib import admin

from . import models


class EntranceExamScorerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'max_level')

admin.site.register(models.EntranceExamScorer, EntranceExamScorerAdmin)


class ProgramTaskScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'scorer', 'task', 'score')

admin.site.register(models.ProgramTaskScore, ProgramTaskScoreAdmin)


class TestCountScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'scorer', 'count', 'score')

admin.site.register(models.TestCountScore, TestCountScoreAdmin)
