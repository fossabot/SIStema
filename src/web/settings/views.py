from django import forms
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from schools.models import School, Session
from . import models
from django.shortcuts import render

import sistema.staff


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


def get_global():
    return list(models.SettingsItem.objects.filter(school__isnull=True, session__isnull=True))


def get_school(school_name):
    result = get_global()
    for item in list(models.SettingsItem.objects.filter(school__short_name=school_name, session__isnull=True)):
        for existing_item in result:
            if existing_item.short_name == item.short_name:
                del existing_item
        result.append(item)
    return result


def get_session(school_name, session_name):
    result = get_school(school_name)
    for item in list(models.SettingsItem.objects.filter(school__isnull=True,
                                                        session__short_name=session_name,
                                                        session__school__short_name=school_name)):
        print(str(item))
        for existing_item in result:
            if existing_item.short_name == item.short_name:
                del existing_item
        result.append(item)
    return result


@sistema.staff.only_staff
def global_settings_list(request):
    settings_list = get_global()
    groups = groups_list_from_settings_list(settings_list)
    return render(request, 'settings/list.html', {'apps': groups, 'area': 'global'})


@sistema.staff.only_staff
def school_settings_list(request, school_name):
    settings_list = get_school(school_name)
    groups = groups_list_from_settings_list(settings_list)
    return render(request, 'settings/list.html', {'apps': groups, 'area': 'school', 'name': school_name})


@sistema.staff.only_staff
def session_settings_list(request, school_name, session_name):
    settings_list = get_session(school_name, session_name)
    groups = groups_list_from_settings_list(settings_list)
    return render(request, 'settings/list.html', {'apps': groups, 'area': 'session', 'name': session_name})


def edit_setting_item(request):
    try:
        id = request.POST['setting_item_id']
    except ValueError:
        return JsonResponse({'status': 'failed', 'error': 'arguments missing'})

    item = get_object_or_404(models.SettingsItem, id=id)
    form_class = type('SettingsItemForm', (forms.Form,), {'value': item.get_form_field()})
    form = form_class(data=request.POST)
    if form.is_valid():
        item.value = form.cleaned_data['value']
        item.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'failed', 'error': ', '.join(form.errors)})
