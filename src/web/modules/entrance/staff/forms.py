from django import forms

import sistema.forms


class FileEntranceExamTasksMarkForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, tasks, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for task in tasks:
            field_id = 'tasks__file__mark_%d' % task.id
            self.fields[field_id] = forms.IntegerField(min_value=0,
                                                       max_value=5,
                                                       widget=forms.HiddenInput(attrs={'id': field_id}))


class EntranceCommentForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    comment = forms.CharField(widget=sistema.forms.TextareaWithFaIcon(attrs={'fa': 'comment'}),
                              label='Комментарий')


class PutIntoCheckingGroupForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, groups, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'] = forms.ChoiceField(widget=forms.Select(), choices=list(groups))

