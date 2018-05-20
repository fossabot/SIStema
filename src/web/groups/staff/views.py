from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
import django.urls

from frontend.table import A
from groups import models
import sistema.staff
import frontend.table
import frontend.icons


class GroupMembersTable(frontend.table.Table):
    index = frontend.table.IndexColumn(verbose_name='')

    name = frontend.table.Column(
        accessor='get_full_name',
        verbose_name='Имя',
        order_by=('profile.last_name', 'profile.first_name'),
        search_in=('profile.first_name', 'profile.last_name')
    )

    city = frontend.table.Column(
        accessor='profile.city',
        orderable=True,
        searchable=True,
        verbose_name='Город'
    )

    def __init__(self, group, *args, **kwargs):
        qs = group.users.order_by(
            'profile__last_name',
            'profile__first_name',
        ).select_related('profile')

        data_url = django.urls.reverse(
            'school:groups:members_data',
            args=[group.school.short_name, group.short_name]
        )

        super().__init__(qs, data_url, *args, **kwargs)

    class Meta:
        icon = frontend.icons.FaIcon('user')
        title = 'Участники группы'
        pagination = (100, 500)


@sistema.staff.only_staff
def group_info(request, group_name):
    group = get_object_or_404(
        models.AbstractGroup,
        school=request.school,
        short_name=group_name
    )

    access_type = group.get_access_type_for_user(request.user)
    if access_type < models.GroupAccess.Type.LIST_MEMBERS:
        return HttpResponseNotFound()

    table = GroupMembersTable(group)
    frontend.table.RequestConfig(request).configure(table)

    return render(request, 'groups/staff/group.html', {
        'group': group,
        'table': table
    })


@sistema.staff.only_staff
def members_data(request, group_name):
    group = get_object_or_404(
        models.AbstractGroup,
        school=request.school,
        short_name=group_name
    )

    access_type = group.get_access_type_for_user(request.user)
    if access_type < models.GroupAccess.Type.LIST_MEMBERS:
        return HttpResponseNotFound()

    table = GroupMembersTable(group)
    return frontend.table.TableDataSource(table).get_response(request)


class GroupsListTable(frontend.table.Table):
    index = frontend.table.IndexColumn(verbose_name='')

    name = frontend.table.TemplateColumn(
        template_name='groups/staff/_groups_list_group_name.html',
        # TODO (andgein): it's hack to get current object as accessor.
        # Null and empty accessor don't work, but I don't know why
        accessor='abstractgroup_ptr.get_real_instance',
        verbose_name='Имя',
        orderable=True,
        order_by='name',
        searchable=True,
        search_in='name'
    )

    description = frontend.table.Column(
        accessor='description',
        orderable=True,
        searchable=True,
        verbose_name='Описание'
    )

    members_count = frontend.table.Column(
        # TODO (andgein): it's hack to get current object as accessor.
        # Null and empty accessor don't work, but I don't know why
        accessor='abstractgroup_ptr.get_real_instance',
        verbose_name='Участников',
    )

    def __init__(self, school, user, *args, **kwargs):
        visible_group_ids = []
        school_groups = models.AbstractGroup.objects.filter(school=school)
        for group in school_groups:
            # Now following line produces extra query for each group.
            # TODO (andgein): make one smart query to database to fetch
            # all groups visible to current user
            if group.get_access_type_for_user(user) >= models.GroupAccess.Type.LIST_MEMBERS:
                visible_group_ids.append(group.id)

        qs = (
            models.AbstractGroup.objects
                .select_related('school')
                .filter(id__in=visible_group_ids).order_by(
                    'name',
                    'description',
                )
        )

        data_url = django.urls.reverse(
            'school:groups:list_data',
            args=[school.short_name]
        )

        super().__init__(qs, data_url, *args, **kwargs)

    class Meta:
        icon = frontend.icons.FaIcon('group')
        title = 'Группы'
        pagination = False

    def render_members_count(self, value):
        return str(len(value.user_ids))


@sistema.staff.only_staff
def groups_list(request):
    table = GroupsListTable(request.school, request.user)
    frontend.table.RequestConfig(request).configure(table)

    return render(request, 'groups/staff/groups.html', {
        'school': request.school,
        'table': table
    })


@sistema.staff.only_staff
def groups_list_data(request):
    table = GroupsListTable(request.school, request.user)
    return frontend.table.TableDataSource(table).get_response(request)
