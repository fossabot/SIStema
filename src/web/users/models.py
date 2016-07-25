from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import crypto


def generate_random_secret_string():
    return crypto.get_random_string(length=32)


class User(auth_models.AbstractUser):
    email_confirmation_token = models.CharField(default=generate_random_secret_string, max_length=32)

    is_email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s (%s)' % (self.last_name, self.first_name, self.email)

    class Meta(auth_models.AbstractUser.Meta):
        pass


class UserPasswordRecovery(models.Model):
    user = models.ForeignKey(User)

    recovery_token = models.CharField(default=generate_random_secret_string, max_length=32)

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


