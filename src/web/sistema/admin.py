import django.forms
from django.utils.text import capfirst

import users.models
import frontend.forms


class ModelAutocompleteField(django.forms.ModelChoiceField):
    def __init__(self, model, url, placeholder, *args, **kwargs):
        super().__init__(queryset=model.objects.all(),
                         empty_label='----------------------------------------',
                         widget=frontend.forms.ModelAutocompleteSelect2(
                             url=url,
                             attrs={
                                 'data-placeholder': placeholder,
                                 'data-html': 'true',
                             },
                         ),
                         *args, **kwargs)


class AutocompleteModelAdminMixIn:
    # Override model, url and placeholder in subclass
    object_model = None
    url = ''
    placeholder = 'Выберите объект'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        related_model = db_field.related_model
        if related_model is self.object_model:
            return ModelAutocompleteField(
                self.object_model,
                self.url,
                self.placeholder,
                required=not db_field.blank,
                label=capfirst(db_field.verbose_name),
                help_text=db_field.help_text
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

