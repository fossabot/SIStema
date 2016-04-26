# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0008_auto_20160328_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='close_time',
            field=models.DateTimeField(default=None, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='short_name',
            field=models.CharField(max_length=100, help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием'),
        ),
    ]
