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
    list_display = ('id', 'user', 'group', 'is_actual')
    list_filter = ('group', 'is_actual')

admin.site.register(models.UserInCheckingGroup, UserInCheckingGroupAdmin)


class CheckingLockAdmin(admin.ModelAdmin):
    list_display = ('id', 'locked_user', 'locked_by', 'locked_until')
    list_filter = (('locked_by', admin.RelatedOnlyFieldListFilter), )

admin.site.register(models.CheckingLock, CheckingLockAdmin)


class SolutionScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'solution', 'scored_by', 'score', 'created_at')
    list_filter = (('scored_by', admin.RelatedOnlyFieldListFilter), )

admin.site.register(models.SolutionScore, SolutionScoreAdmin)


class CheckingCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'for_user', 'commented_by', 'comment', 'created_at')
    list_filter = ('for_school', ('commented_by', admin.RelatedOnlyFieldListFilter))
    search_fields = ('for_user__first_name', 'for_user__last_name', 'for_user__username')

admin.site.register(models.CheckingComment, CheckingCommentAdmin)


class EntranceRecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'for_user', 'checked_by', 'parallel', 'created_at')
    list_filter = ('for_school', ('checked_by', admin.RelatedOnlyFieldListFilter))
    search_fields = ('for_user__first_name', 'for_user__last_name', 'for_user__username')

admin.site.register(models.EntranceRecommendation, EntranceRecommendationAdmin)


class EntranceStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'for_user', 'created_by', 'public_comment', 'is_status_visible', 'status', 'session', 'parallel', 'created_at', 'updated_at')
    list_filter = ('status', 'session', 'parallel', ('created_by', admin.RelatedOnlyFieldListFilter))
    search_fields = ('for_user__first_name', 'for_user__last_name', 'for_user__username')

admin.site.register(models.EntranceStatus, EntranceStatusAdmin)
