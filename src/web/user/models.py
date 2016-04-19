from django.contrib import auth
from django.db import models
from django.utils import crypto


def generate_random_secret_string():
    return crypto.get_random_string(length=32)


class User(auth.models.AbstractUser):
    city = models.CharField(max_length=100)

    email_confirmation_token = models.CharField(default=generate_random_secret_string, max_length=32)

    is_email_confirmed = models.BooleanField(default=False)

    class Meta(auth.models.AbstractUser.Meta):
        pass


class UserPasswordRecovery(models.Model):
    user = models.ForeignKey(User)

    recovery_token = models.CharField(default=generate_random_secret_string, max_length=32)

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


