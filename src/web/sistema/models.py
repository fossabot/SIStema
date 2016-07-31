from django.conf import settings
from polymorphic.models import PolymorphicModel
from django.db import models

from schools.models import School, Session


class DjangoSettingsReference(object):
    """
    For usage in models.FilePathField or similar field.
    If you use models.FilePathField(path=settings.UPLOAD_DIR) it will be saved in migration as
        models.FilePathField(path='/home/user/projects/.../upload')

    Use DjangoSettingsReference for storing it as a settings's reference, i.e.
    models.FilePathField(path=DjangoSettingsReference('UPLOAD_DIR')). It will be saved in migration as
        models.FilePathField(path=DjangoSettingsReference('UPLOAD_DIR'))
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return getattr(settings, self.name)

    def deconstruct(self):
        return "%s.%s" % (__name__, self.__class__.__name__), (self.name,), {}


class SettingsItem(PolymorphicModel):
    name = models.CharField(max_length=100)

    display_name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    school = models.ForeignKey(School, null=True, blank=True, default=None)

    session = models.ForeignKey(Session, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.school is not None and self.session is not None:
            if self.school_id != self.session.school_id:
                raise ValueError("sistema.models: session field value contadicts school field value")

        super().save()


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


class DateSettingsItem(SettingsItem):
    value = models.DateField()
