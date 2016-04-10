from django.contrib import admin

from . import models


class EntranceLevelUpgradeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'get_school',
        'upgraded_to',
        'created_at'
    )

    def get_school(self, obj):
        return obj.upgraded_to.for_school


class SolveTaskEntranceLevelUpgradeRequirementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'base_level',
        'task',
    )


admin.site.register(models.TestEntranceExamTask)
admin.site.register(models.FileEntranceExamTask)
admin.site.register(models.ProgramEntranceExamTask)
admin.site.register(models.EntranceExam)

admin.site.register(models.EntranceLevel)
admin.site.register(models.EntranceStep)

admin.site.register(models.EntranceExamTaskSolution)
admin.site.register(models.ProgramEntranceExamTaskSolution)

admin.site.register(models.EntranceLevelUpgrade, EntranceLevelUpgradeAdmin)
admin.site.register(models.SolveTaskEntranceLevelUpgradeRequirement,
                    SolveTaskEntranceLevelUpgradeRequirementAdmin)
