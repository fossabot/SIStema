from django.contrib import auth
from django.db import models
from django.utils import crypto


def generate_email_confirmation_token():
    return crypto.get_random_string(length=32)


class User(auth.models.AbstractUser):
    city = models.CharField(max_length=100)
    email_confirmation_token = models.CharField(default=generate_email_confirmation_token, max_length=32)
    is_email_confirmed = models.BooleanField(default=False)

    class Meta(auth.models.AbstractUser.Meta):
        pass
