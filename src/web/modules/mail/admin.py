from django.contrib import admin

from . import models


class PersonalEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email_name', 'hash', 'is_active', 'owner')


admin.site.register(models.PersonalEmail, PersonalEmailAdmin)


