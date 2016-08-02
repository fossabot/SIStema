from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render

import sistema.staff
from . import models


def groups_list_from_settings_list(settings):
    apps = dict()
    for setting in settings:
        if setting.app not in apps:
            apps[setting.app] = {'groups': [], 'non_groups': []}
        app_dict = apps[setting.app]
        if setting.group is None:
            app_dict['non_groups'].append(setting)
        else:
            group = setting.group
            if group not in app_dict['groups']:
                app_dict['groups'].append(group)
    return apps


@sistema.staff.only_staff
def global_settings_list(request):
    settings_list = models.SettingsItem.objects.filter(school__isnull=True, session__isnull=True)
    groups = groups_list_from_settings_list(settings_list)
    return render(request, 'settings/list.html', {'apps': groups, 'area': 'global'})


@sistema.staff.only_staff
def school_settings_list(request, school_name):
    settings_list = models.SettingsItem.objects.filter(school__isnull=False, session__isnull=True)
    groups = groups_list_from_settings_list(settings_list)
    return render(request, 'settings/list.html', {'apps': groups, 'area': 'school', 'name': school_name})


@sistema.staff.only_staff
def session_settings_list(request, school_name, session_name):
    settings_list = models.SettingsItem.objects.filter(school__isnull=True, session__isnull=False)
    groups = groups_list_from_settings_list(settings_list)
    return render(request, 'settings/list.html', {'apps': groups, 'area': 'session', 'name': session_name})
