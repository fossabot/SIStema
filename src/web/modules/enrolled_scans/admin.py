from django.contrib import admin

from . import models


class EnrolledScanRequirementAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'name')
    list_filter = ('for_school', )

admin.site.register(models.EnrolledScanRequirement, EnrolledScanRequirementAdmin)


class EnrolledScanAdmin(admin.ModelAdmin):
    list_display = ('id', 'requirement', 'for_user')
    list_filter = ('requirement__for_school', 'requirement')

admin.site.register(models.EnrolledScan, EnrolledScanAdmin)
