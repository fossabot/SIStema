from django.contrib import admin

from . import models


class EntranceExamTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'exam')


class TestEntranceExamTaskAdmin(EntranceExamTaskAdmin):
    pass

admin.site.register(models.TestEntranceExamTask, TestEntranceExamTaskAdmin)


class FileEntranceExamTaskAdmin(EntranceExamTaskAdmin):
    pass

admin.site.register(models.FileEntranceExamTask, FileEntranceExamTaskAdmin)


class ProgramEntranceExamTaskAdmin(EntranceExamTaskAdmin):
    pass

admin.site.register(models.ProgramEntranceExamTask, ProgramEntranceExamTaskAdmin)

admin.site.register(models.EntranceExam)


class EntranceLevelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'short_name',
        'name',
        'order',
        'for_school',
    )

admin.site.register(models.EntranceLevel, EntranceLevelAdmin)

admin.site.register(models.EntranceStep)


class EntranceExamTaskSolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'user', 'ip')
    list_filter = ('task',)
    search_fields = (
        '=user__username',
        '=user__email',
        '=user__first_name',
        '=user__last_name',
        '=ip',
    )

admin.site.register(models.EntranceExamTaskSolution, EntranceExamTaskSolutionAdmin)


class ProgramEntranceExamTaskSolutionAdmin(EntranceExamTaskSolutionAdmin):
    list_display = EntranceExamTaskSolutionAdmin.list_display + (
        'language',
        'ejudge_queue_element',
    )

    list_filter = EntranceExamTaskSolutionAdmin.list_filter + (
        'language',
    )

admin.site.register(models.ProgramEntranceExamTaskSolution, ProgramEntranceExamTaskSolutionAdmin)


class EntranceLevelUpgradeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'get_school',
        'upgraded_to',
        'created_at'
    )

    list_filter = ('upgraded_to',)
    search_fields = (
        '=user__username',
        '=user__email',
        '=user__first_name',
        '=user__last_name',
    )

    def get_school(self, obj):
        return obj.upgraded_to.for_school

admin.site.register(models.EntranceLevelUpgrade, EntranceLevelUpgradeAdmin)


class SolveTaskEntranceLevelUpgradeRequirementAdmin(admin.ModelAdmin):
    list_display = ('id', 'base_level', 'task')
    list_filter = ('base_level', 'task')

admin.site.register(models.SolveTaskEntranceLevelUpgradeRequirement,
                    SolveTaskEntranceLevelUpgradeRequirementAdmin)


class CheckingGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'short_name', 'name')
    list_filter = ('for_school', )

admin.site.register(models.CheckingGroup, CheckingGroupAdmin)


class UserInCheckingGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group')
    list_filter = ('group', )

admin.site.register(models.UserInCheckingGroup, UserInCheckingGroupAdmin)
