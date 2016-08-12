from django.apps import AppConfig, apps


class SettingsConfig(AppConfig):
    name = 'settings'

    def ready(self):
        for app_config in apps.get_app_configs():
            if not hasattr(app_config, 'sistema_settings'):
                continue
            app_name = app_config.name
            for settings_item in app_config.sistema_settings:
                try:
                    settings_item.register(app_name=app_name, settings_config=self)
                except Exception:
                    print('Settings not registered, database empty')
