from django.http import HttpResponse
from django.shortcuts import render

from . import models


def groups_list_from_settings_list(settings):
    apps = dict()
    for setting in settings:
        if setting.app not in apps:
            apps[setting.app] = {"groups": [], "non_groups": []}
        app_dict = apps[setting.app]
        if setting.group is None:
            app_dict["non_groups"].append(setting)
        else:
            group = setting.group
            if group not in app_dict["groups"]:
                app_dict["groups"][group] = []
            app_dict["groups"][group].append(setting)
    return apps


def global_settings_list(request):
    settings_list = models.SettingsItem.objects.filter(school__isnull=True, session__isnull=True)
    print(settings_list)
    groups = groups_list_from_settings_list(settings_list)
    print(groups)
    return render(request, 'settings/list.html', {'apps': groups, 'area': 'global'})


def school_settings_list(request, school_name):
    settings_list = models.SettingsItem.objects.filter(school__isnull=False, session__isnull=True)
    groups = groups_list_from_settings_list(settings_list)
    return render(request, 'settings/list.html', {'apps': groups, 'area': 'school', 'name': school_name})


def session_settings_list(request, school_name, session_name):
    settings_list = models.SettingsItem.objects.filter(school__isnull=True, session__isnull=False)
    groups = groups_list_from_settings_list(settings_list)
    return render(request, 'settings/list.html', {'apps ': groups, 'area': 'session', 'name': session_name})
