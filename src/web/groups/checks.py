from django.core.checks import Error, register
from django.apps import apps


@register()
def check_groups_in_app_configs(app_configs, **kwargs):
    if app_configs is None:
        app_configs = apps.get_app_configs()

    errors = []
    for app_config in app_configs:
        if not hasattr(app_config, 'sistema_groups'):
            continue

        groups = app_config.sistema_groups
        if type(groups) is not dict:
            errors.append(Error(
                'AppConfig.sistema_groups should be dict',
                obj=app_config,
                id='groups.E001',
            ))
            break

        for group_name, group in groups.items():
            if type(group_name) is not str:
                errors.append(Error(
                    'Group\'s short_name should be str, not %s' % (
                        type(group_name),
                    ),
                    obj=app_config,
                    id='groups.E002',
                ))

            if len(group_name) > 100:
                errors.append(Error(
                    'Group\'s short_name can\'t be more then 100 chars',
                    obj=app_config,
                    id='groups.E003',
                ))
                break

            if type(group) is not dict:
                errors.append(Error(
                    'AppConfig.sistema_groups should be dict, '
                    'which values are dicts, but sistema_groups["%s"] is %s' % (
                        group_name, type(group)
                    ),
                    obj=app_config,
                    id='groups.E004',
                ))
                break

            label = group.pop('label', '')
            if type(label) is not str:
                errors.append(Error(
                    'Group\'s label should be str, not %s' % (type(label), ),
                    obj=app_config,
                    id='groups.E005',
                ))
                break

            if len(label) > 30:
                errors.append(Error(
                    'Group\'s label can\'t be more then 30 chars',
                    obj=app_config,
                    id='groups.E006',
                ))
                break

            description = group.pop('description', '')
            if type(description) is not str:
                errors.append(Error(
                    'Group\'s description should be str, not %s' % (
                        type(description),
                    ),
                    obj=app_config,
                    id='groups.E007',
                ))
                break

            auto_members = group.pop('auto_members', [])
            if type(auto_members) not in (list, tuple):
                errors.append(Error(
                    'Group\'s auto_members should be tuple or list, not %s' % (
                        type(auto_members),
                    ),
                    obj=app_config,
                    id='groups.E008',
                ))
                break

            auto_access = group.pop('auto_access', {})
            if type(auto_access) is not dict:
                errors.append(Error(
                    'Group\'s auto_access should be dict, not %s' % (
                        type(auto_access),
                    ),
                    obj=app_config,
                    id='groups.E009',
                ))
                break

            system_wide = group.pop('system_wide', False)
            if type(system_wide) is not bool:
                errors.append(Error(
                    'Group\'s system_wide should be bool, not %s' % (
                        type(system_wide),
                    ),
                    obj=app_config,
                    id='groups.E010',
                ))
                break

    return errors
