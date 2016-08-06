from django import forms


class EditForm(forms.Form):
    value_field = forms.Field()

    def __init__(self, settings_item, data):
        super().__init__(data)
        self.value_field = settings_item.get_form_field()