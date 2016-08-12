from django.apps import AppConfig

from settings.api import IntegerItem, CharItem


class MailConfig(AppConfig):
    name = 'modules.mail'
    sistema_settings = [
        IntegerItem(short_name='max_letter_size_bytes', display_name='Maximum letter size in bytes',
                    description='', default_value=10 * 1024 * 1024),
        IntegerItem(short_name='max_attachments_size_bytes', display_name='Maximum attachments size in bytes',
                    description='', default_value=10 * 1024 * 1024),
        IntegerItem(short_name='max_attachments', display_name='Maximum number of attachments',
                    description='', default_value=10),
        IntegerItem(short_name='max_recipients', display_name='Maximum number of recipients',
                    description='', default_value=5),
        IntegerItem(short_name='size_quota', display_name='Size quota per session in bytes',
                    description='Size which each user has per one session. It\'s spent on sending e-mails.',
                    default_value=50 * 1024 * 1024),
        CharItem(short_name='mail_domain', display_name='Mail domain',
                    description='', default_value='@sistema.lksh.ru'),
    ]
