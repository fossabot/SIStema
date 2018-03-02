# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0007_use_dates_app_1_20171114_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='close_time',
        ),
        migrations.RenameField(
            model_name='questionnaire',
            old_name='close_time_key_date',
            new_name='close_time',
        )
    ]
