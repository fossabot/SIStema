from django import forms
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from . import models


def index(request):
    return HttpResponse('hello, world')


def edit_setting_item(request):
    try:
        id = request.POST['setting_item_id']
    except ValueError:
        return JsonResponse({'status': 'failed', 'error': 'arguments missing'})

    item = get_object_or_404(models.SettingsItem, id=id)
    form_class = type('SettingsItemForm', (forms.Form, ), {'value': item.get_form_field()})
    form = form_class(data=request.POST)
    if form.is_valid():
        item.value = form.cleaned_data['value']
        item.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'failed', 'error': ', '.join(form.errors)})
