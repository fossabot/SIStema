from django.contrib import admin

from . import models


class ContactListAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
    )


class ContactRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'person',
        'contact_list',
    )

    list_filter = (
        'contact_list',
    )


class SisEmailUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )


class ExternalEmailUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'display_name',
        'email',
    )


admin.site.register(models.SisEmailUser, SisEmailUserAdmin)
admin.site.register(models.ExternalEmailUser, ExternalEmailUserAdmin)
admin.site.register(models.ContactList, ContactListAdmin)
admin.site.register(models.ContactRecord, ContactRecordAdmin)