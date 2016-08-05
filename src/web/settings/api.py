class AbstractSettingsItem:
    model_name = None

    def __init__(self, short_name=None, display_name=None, description=None, default_value=None):
        self.short_name = short_name
        self.display_name = display_name
        self.description = description
        self.default_value = default_value
        self.model = None

    def register(self, app_name='sistema', app_config=None):
        self.model = app_config.get_model(self.model_name)
        result = self.model.objects.filter(short_name=self.short_name)
        if not result:
            self.model(short_name=self.short_name, display_name=self.display_name,
                       description=self.description, value=self.default_value,
                       app=app_name).save()


class IntegerItem(AbstractSettingsItem):
    model_name = 'IntegerSettingsItem'


class BigIntegerItem(AbstractSettingsItem):
    model_name = 'BigIntegerSettingsItem'


class DateItem(AbstractSettingsItem):
    model_name = 'DateSettingsItem'


class DateTimeItem(AbstractSettingsItem):
    model_name = 'DateTimeSettingsItem'


class CharItem(AbstractSettingsItem):
    model_name = 'CharSettingsItem'


class TextItem(AbstractSettingsItem):
    model_name = 'TextSettingsItem'


def get_settings(app_name, setting_name, setting_area=None):
    from schools.models import School, Session
    from .models import SettingsItem

    if type(setting_area) is Session:
        setting_item = SettingsItem.objects.filter(short_name=setting_name, app=app_name, session__id=setting_area.id)
        if setting_item is not None:
            return setting_item[0].value

    if type(setting_area) is School:
        setting_item = SettingsItem.objects.filter(short_name=setting_name, app=app_name, school__id=setting_area.id)
        if setting_item is not None:
            return setting_item[0].value

    return SettingsItem.objects.filter(short_name=setting_name, app=app_name)[0].value
