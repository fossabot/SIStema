from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from anymail import exceptions

TEST_MAIL_SUBJECT = "Do you know Taylor Swift?"
TEST_MAIL_TEXT = """You said, "I remember how we felt sitting by the water.
And every time I look at you, it’s like the first time.
I fell in love with a careless man’s careful daughter.
She is the best thing that’s ever been mine."
"""
TEST_MAIL_SENDER = "Anymail Sender <taylor@sandboxb3b7be733f4a4a4c934d36f595d643f1.mailgun.org>"


class Command(BaseCommand):
    help = 'Sends test email'

    def add_arguments(self, parser):
        parser.add_argument('recipient', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            send_mail(TEST_MAIL_SUBJECT, TEST_MAIL_TEXT, TEST_MAIL_SENDER, [' '.join(options['recipient'])])
        except exceptions.AnymailAPIError as error:
            print(error.response.text)
        self.stdout.write(self.style.SUCCESS('Message sent'))

