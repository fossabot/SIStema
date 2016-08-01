from django.conf import settings
from polymorphic.models import PolymorphicModel

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
