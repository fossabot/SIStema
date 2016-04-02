from django.contrib import admin

from hijack.admin import HijackUserAdminMixin
from reversion.admin import VersionAdmin

from . import models


class UserAdmin(VersionAdmin, HijackUserAdminMixin):
    list_display = (
        'id',
        'username',
        'email',
        'is_superuser',
        'is_staff',
        'hijack_field',
    )


admin.site.register(models.User, UserAdmin)
