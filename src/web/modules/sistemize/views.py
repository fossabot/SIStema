# -*- coding: utf-8 -*-

import collections

from django import forms
from django import shortcuts

from questionnaire import models

class NamesForm(forms.Form):
    names_file = forms.FileField(required=False)
    names_list = forms.CharField(
        label="Список имён", required=False, widget=forms.Textarea)


def sistemize(request):
    if request.method == 'POST':
        form = NamesForm(request.POST, request.FILES)
        if form.is_valid():
            if 'names_file' in request.FILES:
                result = get_sistema_ids(
                    request.FILES['names_file'].read().decode('utf-8'))
            else:
                result = get_sistema_ids(form.cleaned_data['names_list'])

            return shortcuts.render(request, 'sistemize/sistemize.html', {
                'form': form,
                'result': result})
    else:
        form = NamesForm()

    return shortcuts.render(request, 'sistemize/sistemize.html', {'form': form})


def get_sistema_ids(names_str):
    many_names = [[normalize_string(name) for name in full_name.split()]
                  for full_name in names_str.split('\n')]

    # question_objects = models.TextQuestionnaireQuestion.objects
    # first_name_question = question_objects.get(short_name='first_name')
    # middle_name_question = question_objects.get(short_name='middle_name')
    # last_name_question = question_objects.get(short_name='last_name')

    uids_by_name = collections.defaultdict(set)
    for q_short_name in ['first_name', 'middle_name', 'last_name']:
        ans_objects = models.QuestionnaireAnswer.objects
        for ans in ans_objects.filter(question_short_name=q_short_name).all():
            name = normalize_string(ans.answer)
            uids_by_name[name].add(ans.user.id)

    result = []
    for names in many_names:
        uids = set(uids_by_name[names[0]])
        for name in names[1:]:
            uids &= uids_by_name[name]

        result.append(','.join(str(x) for x in uids) or '-')

    return result


def normalize_string(string):
    return string.lower().replace('ё', 'е')
