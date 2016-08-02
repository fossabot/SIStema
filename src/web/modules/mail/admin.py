from django.contrib import admin

from . import models


class ContactRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'person',
        'owner',
    )

    list_filter = (
        'owner',
    )


admin.site.register(models.ContactRecord, ContactRecordAdmin)


class SisEmailUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )


admin.site.register(models.SisEmailUser, SisEmailUserAdmin)


class ExternalEmailUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'display_name',
        'email',
    )

admin.site.register(models.ExternalEmailUser, ExternalEmailUserAdmin)


class PersonalEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email_name', 'hash', 'is_active', 'owner')


admin.site.register(models.PersonalEmail, PersonalEmailAdmin)


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'subject', 'created_at')


admin.site.register(models.EmailMessage, EmailMessageAdmin)


