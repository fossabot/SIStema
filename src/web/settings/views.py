from django import forms
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

import sistema.staff
from schools.models import School, Session
from . import models


def groups_list_from_settings_list(settings):
    apps = dict()
    for settings_item in settings:
        settings_item.form = get_form(settings_item)
        if settings_item.app not in apps:
            apps[settings_item.app] = {'groups': [], 'non_groups': []}
        app_dict = apps[settings_item.app]
        if settings_item.group is None:
            app_dict['non_groups'].append(settings_item)
        else:
            group = settings_item.group
            if group not in app_dict['groups']:
                app_dict['groups'].append(group)
    return apps


def get_global_settings():
    return list(models.SettingsItem.objects.filter(school__isnull=True, session__isnull=True))


def get_school_settings(school_name):
    result = get_global_settings()
    for item in list(models.SettingsItem.objects.filter(school__short_name=school_name, session__isnull=True)):
        for existing_item in result:
            if existing_item.short_name == item.short_name:
                result.remove(existing_item)
        result.append(item)
    return result


def get_session_settings(school_name, session_name):
    result = get_school_settings(school_name)
    for item in list(models.SettingsItem.objects.filter(school__isnull=True,
                                                        session__short_name=session_name,
                                                        session__school__short_name=school_name)):
        for existing_item in result:
            if existing_item.short_name == item.short_name:
                result.remove(existing_item)
        result.append(item)
    return result


@sistema.staff.only_staff
def global_settings_list(request):
    settings_list = get_global_settings()
    groups = groups_list_from_settings_list(settings_list)
    return render(request, 'settings/list.html', {'apps': groups, 'area': 'global'})


@sistema.staff.only_staff
def school_settings_list(request, school_name):
    settings_list = get_school_settings(school_name)
    groups = groups_list_from_settings_list(settings_list)
    school = get_object_or_404(School, short_name=school_name)
    sessions = []
    for session in Session.objects.filter(school=school):
        sessions.append({'name': session.name, 'short_name': session.short_name})
    return render(request, 'settings/list.html', {'apps': groups,
                                                  'area': 'school',
                                                  'name': school.name,
                                                  'short_name': school.short_name,
                                                  'sessions': sessions})


@sistema.staff.only_staff
def session_settings_list(request, school_name, session_name):
    settings_list = get_session_settings(school_name, session_name)
    groups = groups_list_from_settings_list(settings_list)
    school = get_object_or_404(School, short_name=school_name)
    session = get_object_or_404(Session, school=school, short_name=session_name)
    return render(request, 'settings/list.html', {'apps': groups,
                                                  'area': 'session',
                                                  'name': str(session),
                                                  'school_short_name': school.short_name})


@sistema.staff.only_staff
def edit_settings_item(request, id):
    item = get_object_or_404(models.SettingsItem, id=id)
    form = get_form(item, request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        item.value = form.cleaned_data['value_field']
        item.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'failed', 'error': ', '.join(form.errors)})


@sistema.staff.only_staff
def specify_settings_area(request, id, school_name, session_name):
    item = get_object_or_404(models.SettingsItem, id=id)
    item.session = None
    item.school = None
    if school_name is not None and session_name is None:
        item.school = get_object_or_404(models.School, short_name=school_name)
    elif session_name is not None:
        item.session = get_object_or_404(models.Session, short_name=session_name, school__short_name=school_name)
    item.id = None
    form = get_form(item, request.POST)
    if form.is_valid():
        item.value = form.cleaned_data['value_field']
        try:
            item.save()
        except IntegrityError:
            return JsonResponse({'status': 'failed', 'error': 'the scope hasn\'t changed'})
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'failed', 'error': ', '.join(form.errors)})


@sistema.staff.only_staff
def clone_settings_item(request, id, school_name, session_name):
    item = get_object_or_404(models.SettingsItem, id=id)
    model = type(item)
    new_item = model(   short_name=item.short_name, display_name=item.display_name, description=item.description,
                        value=item.value, app=item.app, group=item.group, school=item.school, session=item.session)
    new_item.save()
    item.parent = new_item
    item.save()
    return specify_settings_area(request, id, school_name, session_name)


def get_form(settings_item, data=None):
    form_class = type('SettingsItemForm', (forms.Form,), {'value_field': settings_item.get_form_field()})
    return form_class(data)


def process_edit_request(request, settings_item_id, school_name=None, session_name=None):
    item = get_object_or_404(models.SettingsItem, id=settings_item_id)
    if item.school is None and item.session is None:
        if school_name is None and session_name is None:
            return edit_settings_item(request, settings_item_id)
        return clone_settings_item(request, settings_item_id, school_name, session_name)
    if item.session is None:
        if school_name is None and session_name is None:
            return JsonResponse({'status': 'failed', 'error': 'cannot clone to globals'})
        if school_name == item.school.short_name and session_name is None:
            return edit_settings_item(request, settings_item_id)
        return clone_settings_item(request, settings_item_id, school_name, session_name)
    if session_name is None:
        return JsonResponse({'status': 'failed', 'error': 'cannot clone session settings to global or school settings'})
    if item.session.school.short_name == school_name and item.session.short_name == session_name:
        return edit_settings_item(request, settings_item_id)
    return clone_settings_item(request, settings_item_id, school_name, session_name)
