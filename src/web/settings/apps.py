from django.apps import AppConfig, apps
from .api import TextItem


class SettingsConfig(AppConfig):
    name = 'settings'
    sistema_settings = [
        TextItem(short_name='test_text', display_name='Hahahah', description='Azazaza', default_value='olololo')
    ]

    def ready(self):
        for app_config in apps.get_app_configs():
            if not hasattr(app_config, 'sistema_settings'):
                continue
            if hasattr(app_config, 'verbose_name'):
                app_name = app_config.verbose_name
            else:
                app_name = app_config.name

            for settings_item in app_config.sistema_settings:
                settings_item.register(app_name=app_name, app_config=app_config)

