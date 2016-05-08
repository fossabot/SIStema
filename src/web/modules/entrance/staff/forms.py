from django import forms

import sistema.forms

from .. import models


class FileEntranceExamTasksMarkForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, tasks, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for task in tasks:
            field_id = 'tasks__file__mark_%d' % task.id
            self.fields[field_id] = forms.IntegerField(min_value=0,
                                                       max_value=5,
                                                       widget=forms.HiddenInput(attrs={'id': field_id}))


class EntranceRecommendationForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    comment = forms.CharField(widget=sistema.forms.TextInputWithFaIcon(attrs={'fa': 'comment'}),
                              label='Комментарий')

    score = forms.IntegerField(label='Баллы', initial=0)

    # TODO: choose school as a parameter
    def __init__(self, parallels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_parallels = [('-', 'Не зачислить')] + list(parallels)
        self.fields['recommended_parallel'] = forms.ChoiceField(widget=forms.Select(),
                                                                choices=available_parallels,
                                                                label='Рекомендованная параллель')


class PutIntoCheckingGroupForm(forms.Form):
    def __init__(self, school, *args, **kwargs):
        super().__init__(*args, **kwargs)

        groups = models.CheckingGroup.objects.filter(for_school=school)
        groups = [(g.id, g.name) for g in groups]
        self.fields['group_id'] = forms.ChoiceField(widget=forms.Select(), choices=list(groups))

