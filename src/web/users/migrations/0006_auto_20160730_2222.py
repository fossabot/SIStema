# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-30 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20160728_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_email_confirmed',
            field=models.BooleanField(default=True),
        ),
    ]
