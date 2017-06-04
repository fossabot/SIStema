from django.contrib import admin
from django.db import models
import django.forms

from dal import autocomplete


def register_autocomplete_field_for_foreign_key(
        model_cls,
        url,
        queryset=None,
        placeholder='Поиск...',
        empty_label='----------------------------------------'):
    if queryset is None:
        queryset = model_cls.objects.all()

    form_field = django.forms.ModelChoiceField(
        queryset=queryset,
        empty_label=empty_label,
        widget=autocomplete.ModelSelect2(
            url=url,
            attrs={'data-placeholder': placeholder, 'data-html': 'true'}
        )
    )

    register_form_field_for_foreign_key(model_cls, form_field)


def register_form_field_for_foreign_key(model_cls, form_field):
    SistemaAdminMixin.register_form_field_for_foreign_key(model_cls, form_field)


class SistemaAdminMixin:
    form_fields_for_foreign_keys = []

    @classmethod
    def register_form_field_for_foreign_key(cls, model_cls, form_field):
        assert issubclass(model_cls, models.Model)
        cls.form_fields_for_foreign_keys.append((model_cls, form_field))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        for model_cls, form_field in self.form_fields_for_foreign_keys:
            if db_field.related_model is model_cls:
                return form_field() if callable(form_field) else form_field
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SistemaModelAdmin(SistemaAdminMixin, admin.ModelAdmin):
    pass
