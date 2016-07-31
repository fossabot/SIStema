from django.contrib import admin
from sistema import models


class SettingsItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'short_name',
        'display_name',
        'description',
        'school',
        'session',
        'value'
    )


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'short_name',
        'display_name',
        'description'
    )


admin.site.register(models.IntegerSettingsItem, SettingsItemAdmin)
admin.site.register(models.BigIntegerSettingsItem, SettingsItemAdmin)
admin.site.register(models.DateSettingsItem, SettingsItemAdmin)
admin.site.register(models.DateTimeSettingsItem, SettingsItemAdmin)
admin.site.register(models.CharSettingsItem, SettingsItemAdmin)
admin.site.register(models.TextSettingsItem, SettingsItemAdmin)
admin.site.register(models.Group, GroupAdmin)