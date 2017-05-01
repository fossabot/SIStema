from django.db import models
from django.utils.functional import cached_property

import djchoices
import polymorphic.models

import schools.models
import users.models


class Group(models.Model):
    school = models.ForeignKey(
        schools.models.School,
        null=True,
        blank=True,
        related_name='groups',
        on_delete=models.CASCADE,
    )

    owner = models.ForeignKey(
        users.models.User,
        null=True,
        blank=True,
        related_name='owned_groups',
        on_delete=models.CASCADE,
        help_text='None, если владелец группы — система'
    )

    short_name = models.CharField(
        max_length=100,
        help_text='Используется в урлах. '
                  'Лучше обойтись латинскими буквами, цифрами и подчёркиванием',
        db_index=True,
    )

    label = models.CharField(
        max_length=30,
        help_text='Покороче, используется на метках'
    )

    description = models.TextField(help_text='Подлинее, подробное описание')

    can_be_deleted = models.BooleanField(
        default=True,
        help_text='Системные группы не могут быть удалены',
    )

    list_members_to_everyone = models.BooleanField(
        default=False,
        help_text='Видны ли всем список участников и принадлежность '
                  'пользователей группе',
    )

    @cached_property
    def group_members(self):
        return (GroupInGroupMembership.objects.filter(group=self)
                .select_related('member'))

    @cached_property
    def user_members(self):
        return (UserInGroupMembership.objects.filter(group=self)
                .select_related('member'))

    @cached_property
    def child(self):
        return self.group_members + self.user_members

    @cached_property
    def members(self):
        members = set()
        visited_groups_ids = {self.id}
        queue = [self]
        for group in queue:
            user_members = [m.member for m in group.user_members]
            members.update(user_members)
            for child_group in group.group_members:
                if child_group.member.id not in visited_groups_ids:
                    visited_groups_ids.add(child_group.member.id)
                    queue.append(child_group.member)
        return list(members)

    def is_user_in_group(self, user):
        return user.id in [u.id for u in self.members]

    @property
    def default_access_type(self):
        if self.list_members_to_everyone:
            return GroupAccessType.LIST_MEMBERS
        return GroupAccessType.NONE

    def get_access_type_for_user(self, user):
        user_access = GroupAccessForUser.objects.filter(
            to_group=self, user=user
        ).first()
        if user_access is None:
            user_access = self.default_access_type
        else:
            user_access = user_access.access_type

        group_accesses = list(GroupAccessForGroup.objects.filter(
            to_group=self
        ).select_related('group').order_by('-access_type'))
        for group_access in group_accesses:
            if user_access > group_access.access_type:
                break

            if group_access.group.is_user_in_group(user):
                return group_access.access_type

        return user_access

    def __str__(self):
        result = 'Группа «%s»' % (self.label, )
        if self.school is not None:
            result += ' для %s' % (str(self.school), )
        return result

    class Meta:
        unique_together = ('short_name', 'school')


class GroupMembership(models.Model):
    group = models.ForeignKey(
        Group,
        related_name='+',
        on_delete=models.CASCADE,
    )

    added_by = models.ForeignKey(
        users.models.User,
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE,
        help_text='Кем добавлен участник группы. None, если добавлено системой.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class GroupInGroupMembership(GroupMembership):
    member = models.ForeignKey(
        Group,
        related_name='member_in_groups',
        on_delete=models.CASCADE,
    )


class UserInGroupMembership(GroupMembership):
    member = models.ForeignKey(
        users.models.User,
        related_name='member_in_groups',
        on_delete=models.CASCADE,
    )


class GroupAccessType(djchoices.DjangoChoices):
    NONE = djchoices.ChoiceItem(
        value=0,
        label='Нет доступа, группа не видна',
    )

    LIST_MEMBERS = djchoices.ChoiceItem(
        value=1,
        label='Может просматривать участников',
    )
    EDIT_MEMBERS = djchoices.ChoiceItem(
        value=2,
        label='Может добавлять и удалять участников',
    )
    ADMIN = djchoices.ChoiceItem(
        value=3,
        label='Полный доступ',
    )


class GroupAccess(polymorphic.models.PolymorphicModel):
    to_group = models.ForeignKey(
        Group,
        related_name='accesses',
        on_delete=models.CASCADE,
    )

    access_type = models.PositiveIntegerField(
        choices=GroupAccessType.choices,
        validators=[GroupAccessType.validator],
        db_index=True,
    )

    added_by = models.ForeignKey(
        users.models.User,
        related_name='+',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='Кем выдан доступ. Если None, то системой'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )


class GroupAccessForUser(GroupAccess):
    user = models.ForeignKey(
        users.models.User,
        related_name='+',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return 'Доступ %s к %s' % (self.user.get_full_name(), self.to_group)


class GroupAccessForGroup(GroupAccess):
    group = models.ForeignKey(
        Group,
        related_name='+',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return 'Доступ участников %s к %s' % (self.group, self.to_group)