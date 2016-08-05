class SettingsItem:
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


class IntegerItem(SettingsItem):
    model_name = 'IntegerSettingsItem'


class BigIntegerItem(SettingsItem):
    model_name = 'BigIntegerSettingsItem'


class DateItem(SettingsItem):
    model_name = 'DateSettingsItem'


class DateTimeItem(SettingsItem):
    model_name = 'DateTimeSettingsItem'


class CharItem(SettingsItem):
    model_name = 'CharSettingsItem'


class TextItem(SettingsItem):
    model_name = 'TextSettingsItem'
