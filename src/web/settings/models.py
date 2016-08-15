from django import forms
from django.db import models
from polymorphic.models import PolymorphicModel

from schools.models import School, Session


class Group(models.Model):
    short_name = models.CharField(
        max_length=100,
        help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием'
    )

    display_name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.display_name


class SettingsItem(PolymorphicModel):
    short_name = models.CharField(
        max_length=100,
        help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием',
    )

    display_name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    school = models.ForeignKey(School, null=True, blank=True, default=None, related_name='settings')

    session = models.ForeignKey(Session, null=True, blank=True, default=None, related_name='settings')

    app = models.CharField(max_length=50)

    group = models.ForeignKey(Group, null=True, blank=True, related_name='items')

    def save(self, *args, **kwargs):
        if self.school_id is not None and self.session_id is not None:
            raise ValueError('sistema.models.SettingsItem: session field value contradicts school field value')
        super().save()


class IntegerSettingsItem(SettingsItem):
    value = models.IntegerField()

    def get_form_field(self):
        return forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        )


class BigIntegerSettingsItem(SettingsItem):
    value = models.BigIntegerField()

    def get_form_field(self):
        return forms.IntegerField(
            max_value=models.BigIntegerField.MAX_BIGINT,
            min_value=-1 - models.BigIntegerField.MAX_BIGINT,
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        )


class PositiveIntegerSettingsItem(SettingsItem):
    value = models.PositiveIntegerField()

    def get_form_field(self):
        return forms.IntegerField(
            min_value=0,
            widget=forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        )


class TextSettingsItem(SettingsItem):
    value = models.TextField()

    def get_form_field(self):
        return forms.CharField(
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5'
            }),
        )


class CharSettingsItem(SettingsItem):
    value = models.CharField(max_length=256)

    def get_form_field(self):
        return forms.CharField(
            max_length=256,
            widget=forms.TextInput(attrs={
                'rows': '1',
                'class': 'form-control',
            }),
        )


class EmailSettingsItem(SettingsItem):
    value = models.EmailField()

    def get_form_field(self):
        return forms.EmailField(
            widget=forms.EmailInput(attrs={
                'class': 'form-control'
            }),
        )


class BooleanSettingsItem(SettingsItem):
    value = models.BooleanField()

    def get_form_field(self):
        return forms.BooleanField(
            widget=forms.CheckboxInput(attrs={
                'class': 'form-control'
            }),
        )


class DateTimeSettingsItem(SettingsItem):
    value = models.DateTimeField()

    def get_form_field(self):
        return forms.DateTimeField(
            widget=forms.DateTimeInput(attrs={
                'class': 'form-control',
                'data-format': 'HH:mm DD.MM.YYYY',
                'data-view-mode': 'years',
                'data-pick-time': 'true',
                'placeholder': '__:__ __.__.____'
            }),
        )


class DateSettingsItem(SettingsItem):
    value = models.DateField()

    def get_form_field(self):
        return forms.DateTimeField(
            widget=forms.DateInput(attrs={
                'class': 'form-control',
                'data-format': 'DD.MM.YYYY',
                'data-view-mode': 'years',
                'data-pick-time': 'false',
                'placeholder': '__.__.____'
            }),
        )
