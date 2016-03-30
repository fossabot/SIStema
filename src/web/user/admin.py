from django.contrib import admin

from reversion.admin import VersionAdmin

from . import models


class UserAdmin(VersionAdmin):
    pass


admin.site.register(models.User, UserAdmin)
