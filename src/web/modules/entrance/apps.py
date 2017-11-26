from django.apps import AppConfig


class EntranceConfig(AppConfig):
    name = 'modules.entrance'

    sistema_groups = {
        'entrance__admins': {
            'name': 'Админы вступительной',
            'description': 'Группа администраторов вступительной работы',
        },
        'entrance__can_check': {
            'name': 'Проверяющие вступительную',
            'description': 'Группа пользователей, '
                           'которые могут проверять вступительную работу: '
                           'смотреть решения школьников, писать к ним комментарии и '
                           'ставить за них баллы',
            'auto_members': ['entrance__admins'],
            'auto_access': {
                'entrance__admins': 'admin',
            }
        },
    }
