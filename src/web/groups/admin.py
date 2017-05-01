from django.contrib import admin
from polymorphic.admin import (PolymorphicChildModelFilter,
                               PolymorphicChildModelAdmin)

import sistema.polymorphic
import sistema.admin
from groups import models


@admin.register(models.Group)
class GroupAdmin(sistema.admin.UserAutocompleteModelAdminMixIn, admin.ModelAdmin):
    list_display = ('id', 'school', 'owner', 'short_name', 'label',
                    'can_be_deleted', )
    list_filter = (('school', admin.RelatedOnlyFieldListFilter), )
    search_fields = (
        'id',
        'owner__first_name',
        'owner__last_name',
        '=owner__email',
        'short_name',
        'label',
        'description'
    )


@admin.register(models.GroupInGroupMembership)
@admin.register(models.UserInGroupMembership)
class GroupMembershipAdmin(sistema.admin.UserAutocompleteModelAdminMixIn,
                           admin.ModelAdmin):
    list_display = ('id', 'group', 'member')
    list_filter = (('group', admin.RelatedOnlyFieldListFilter), )


@admin.register(models.GroupAccess)
class GroupAccessAdmin(sistema.polymorphic.PolymorphicParentModelAdmin):
    base_model = models.GroupAccess
    list_display = ('id', 'get_class', 'to_group', 'access_type',
                    'added_by', 'created_at')
    list_filter = ('to_group__school',
                   'access_type',
                   PolymorphicChildModelFilter)
    ordering = ('to_group__school', '-created_at')


@admin.register(models.GroupAccessForUser)
@admin.register(models.GroupAccessForGroup)
class GroupAccessChildAdmin(sistema.admin.UserAutocompleteModelAdminMixIn,
                            PolymorphicChildModelAdmin):
    base_model = models.GroupAccess

