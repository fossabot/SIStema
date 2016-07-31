from django.contrib import admin

from . import models


class PersonalEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email-name', 'hash', 'is_active', 'owner', 'sessions')


admin.site.register(models.PersonalEmail, PersonalEmailAdmin)


