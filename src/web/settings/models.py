import django
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

    class Meta:
        unique_together = ('short_name', 'school', 'session')

    def save(self, *args, **kwargs):
        if self.school_id is not None and self.session_id is not None:
            raise ValueError('sistema.models.SettingsItem: session field value contradicts school field value')

        super().save()

    def get_form_field(self):
        return self.value.formfield()


class IntegerSettingsItem(SettingsItem):
    value = models.IntegerField()


class BigIntegerSettingsItem(SettingsItem):
    value = models.BigIntegerField()


class PositiveIntegerSettingsItem(SettingsItem):
    value = models.PositiveIntegerField()


class TextSettingsItem(SettingsItem):
    value = models.TextField()


class CharSettingsItem(SettingsItem):
    value = models.CharField(max_length=256)


class EmailSettingsItem(SettingsItem):
    value = models.EmailField()


class DateTimeSettingsItem(SettingsItem):
    value = models.DateTimeField()

    def get_form_field(self):
        return forms.DateTimeField(
            widget=django.forms.DateInput(attrs={
                'class': 'datetimepicker',
                'data-format': 'DD.MM.YYYY',
                'data-view-mode': 'years',
                'data-pick-time': 'false',
                'placeholder': 'дд.мм.гггг',
            }),
        )


class DateSettingsItem(SettingsItem):
    value = models.DateField()

    def get_form_field(self):
        return forms.DateTimeField(
            widget=django.forms.DateInput(attrs={
                'class': 'datetimepicker',
                'data-format': 'DD.MM.YYYY',
                'data-view-mode': 'years',
                'data-pick-time': 'false',
                'placeholder': 'дд.мм.гггг',
            }),
        )
