from django.apps import AppConfig


class EntranceConfig(AppConfig):
    name = 'modules.entrance'

    sistema_groups = {
        'entrance__admins': {
            'label': 'Админы вступительной',
            'description': 'Группа администраторов вступительной работы',
        },
        'entrance__can_check': {
            'label': 'Проверяющие вступительную',
            'description': 'Группа пользователей, '
                           'которые могут проверять вступительную работу: '
                           'смотреть решения школьников, писать комментарии и '
                           'ставить баллы за них',
            'auto_members': ['entrance__admin'],
            'auto_access': {
                'entrance__admin': 'admin',
            }
        },
    }
