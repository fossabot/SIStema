from django.contrib import admin

from . import models


class EnrolledScanRequirementAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'name')
    list_filter = ('school', )

admin.site.register(models.EnrolledScanRequirement, EnrolledScanRequirementAdmin)


class EnrolledScanAdmin(admin.ModelAdmin):
    list_display = ('id', 'requirement', 'user')
    list_filter = ('requirement__school', 'requirement')

admin.site.register(models.EnrolledScan, EnrolledScanAdmin)


class QuestionnaireVariantEnrolledScanRequirementConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'requirement', 'variant')
    list_filter = ('requirement__school', 'requirement')

admin.site.register(models.QuestionnaireVariantEnrolledScanRequirementCondition,
                    QuestionnaireVariantEnrolledScanRequirementConditionAdmin)
