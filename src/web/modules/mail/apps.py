from django.apps import AppConfig

from settings.api import IntegerItem, CharItem, BooleanItem


class MailConfig(AppConfig):
    name = 'modules.mail'
    sistema_settings = [
        IntegerItem(short_name='max_letter_size_bytes', display_name='Максимальный размер письма в байтах',
                    description='', default_value=10 * 1024 * 1024),
        IntegerItem(short_name='max_attachments_size_bytes', display_name='Максимальный суммарный размер аттачментов '
                                                                          'в байтах',
                    description='', default_value=10 * 1024 * 1024),
        IntegerItem(short_name='max_attachments', display_name='Максимальное количество аттачментов',
                    description='', default_value=10),
        IntegerItem(short_name='max_recipients', display_name='Максимальное количество получателей',
                    description='', default_value=5),
        IntegerItem(short_name='size_quota', display_name='Квота на смену в байтах',
                    description='Объём, выдаваемый пользователю на текущую смену. Тратится на посылку писем',
                    default_value=50 * 1024 * 1024),
        CharItem(short_name='mail_domain', display_name='Почтовый домен',
                 description='', default_value='@sistema.lksh.ru'),
        BooleanItem(short_name='send_mails', display_name='Посылать сообщения',
                    description='Посылать ли сообщения во внешний мир',
                    default_value=False),
    ]
