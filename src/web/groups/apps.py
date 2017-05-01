from django.apps import AppConfig, apps
from django.db.models.signals import post_save
from django.db import transaction


class GroupsConfig(AppConfig):
    name = 'groups'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self._auto_access = []
        self._auto_members = []

    def ready(self):
        self._auto_members = []
        self._auto_access = []

        for app_config in apps.get_app_configs():
            if not hasattr(app_config, 'sistema_groups'):
                continue

            groups = app_config.sistema_groups
            for group_name, group in groups.items():
                self._ensure_group_exists(group_name, group)

        for group, auto_members in self._auto_members:
            self._set_auto_members(group, auto_members)

        for group, auto_access in self._auto_access:
            self._set_auto_access(group, auto_access)

        self._set_hook_for_new_school()

    @transaction.atomic
    def _ensure_group_exists(self, group_name, group_params):
        system_wide = group_params.get('system_wide', False)
        if system_wide:
            self._ensure_system_wide_group_exists(group_name, group_params)
        else:
            self._ensure_school_group_exists(group_name, group_params)

    def _ensure_system_wide_group_exists(self, group_name, group_params):
        # You can't import models on module level:
        # https://docs.djangoproject.com/en/1.11/ref/applications/#django.apps.AppConfig.ready
        from groups.models import Group

        group = Group.objects.filter(school__isnull=True,
                                     short_name=group_name).first()
        if group is None:
            self._create_system_wide_group(group_name, group_params)
        else:
            self._update_group(group, group_params)

    def _ensure_school_group_exists(self, group_name, group_params):
        from schools.models import School
        from groups.models import Group

        for school in School.objects.all():
            group = Group.objects.filter(school=school,
                                         short_name=group_name).first()
            if group is None:
                self._create_group(school, group_name, group_params)
            else:
                self._update_group(group, group_params)

    def _create_system_wide_group(self, group_name, group_params):
        self._create_group(None, group_name, group_params)

    def _create_group(self, school, group_name, group_params):
        from groups.models import Group

        group = Group.objects.create(
            school=school,
            short_name=group_name,
            label=group_params.get('label', ''),
            description=group_params.get('description', ''),
            owner=None,
            can_be_deleted=False,
        )

        self._auto_members.append((group, group_params.get('auto_members', [])))
        self._auto_access.append((group, group_params.get('auto_access', {})))

        print('Group #%d [%s] «%s» has been created for school %s' % (
            group.id,
            group.short_name,
            group.label,
            group.school
        ))

    def _update_group(self, group, group_params):
        group.label = group_params.get('label', '')
        group.description = group_params.get('description', '')
        group.owner = None
        group.can_be_deleted = False
        self._auto_members.append((group, group_params.get('auto_members', [])))
        self._auto_access.append((group, group_params.get('auto_access', {})))
        group.save()

    def _set_auto_members(self, group, auto_members):
        from groups.models import Group, GroupInGroupMembership

        for member_group_name in auto_members:
            member_group = Group.objects.filter(
                school=group.school, short_name=member_group_name
            ).first()
            if member_group is None:
                raise LookupError(
                    'Can\'t find group %s for settings auto_member' % (
                        member_group_name,
                    ))

            GroupInGroupMembership.objects.update_or_create(
                group=group,
                member=member_group,
                defaults={
                    'added_by': None,
                }
            )

    def _set_auto_access(self, group, auto_access):
        from groups.models import Group, GroupAccessForGroup, GroupAccessType

        for access_group_name, access_group_access_type in auto_access.items():
            if access_group_access_type == 'admin':
                access_type = GroupAccessType.ADMIN
            elif access_group_access_type == 'list_members':
                access_type = GroupAccessType.LIST_MEMBERS
            elif access_group_access_type == 'edit_members':
                access_type = GroupAccessType.EDIT_MEMBERS
            else:
                raise ValueError(
                    'Invalid access_type in sistema_groups '
                    'for auto_accessed group %s: %s' % (
                        access_group_name,
                        access_group_access_type,
                    ))

            access_group = Group.objects.filter(
                school=group.school, short_name=access_group_name
            ).first()
            if access_group is None:
                raise LookupError(
                    'Can\'t find group %s for settings auto_access' % (
                        access_group_name,
                    ))

            GroupAccessForGroup.objects.update_or_create(
                to_group=group,
                group=access_group,
                defaults={
                    'added_by': None,
                    'access_type': access_type,
                }
            )

    def _set_hook_for_new_school(self):
        post_save.connect(
            lambda school, **kwargs: self._on_new_school(school),
            sender='schools.School'
        )

    def _on_new_school(self, school):
        # Recall self.ready() for creating groups for the new school
        self.ready()
