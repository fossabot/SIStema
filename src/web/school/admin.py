from django.contrib import admin

from reversion.admin import VersionAdmin

from . import models


class SchoolAdmin(VersionAdmin):
    pass


class SessionAdmin(VersionAdmin):
    pass


admin.site.register(models.School, SchoolAdmin)
admin.site.register(models.Session, SessionAdmin)
