# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import djchoices.choices


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
                model_name='user',
                name='username',
                field=models.CharField(max_length=100, help_text='Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.')
        ),
    ]
