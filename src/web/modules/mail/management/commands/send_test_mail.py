from django.core.management.base import BaseCommand
from django.core.mail import send_mail

TEST_MAIL_SUBJECT = "Do you know Taylor Swift?"
TEST_MAIL_TEXT = """You said, "I remember how we felt sitting by the water.
And every time I look at you, it’s like the first time.
I fell in love with a careless man’s careful daughter.
She is the best thing that’s ever been mine."
"""
TEST_MAIL_SENDER = "Anymail Sender <taylor@lksh.ru>"


class Command(BaseCommand):
    help = 'Sends test email'

    def add_arguments(self, parser):
        parser.add_argument('recipient', nargs='+', type=str)

    def handle(self, *args, **options):
        send_mail(TEST_MAIL_SUBJECT, TEST_MAIL_TEXT, TEST_MAIL_SENDER, [options['recipient']])
        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"'))

