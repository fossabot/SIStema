# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0052_use_dates_app_1_20171115_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractentrancestep',
            name='available_from_time',
        ),
        migrations.RemoveField(
            model_name='abstractentrancestep',
            name='available_to_time',
        ),
        migrations.RenameField(
            model_name='abstractentrancestep',
            old_name='available_from_time_key_date',
            new_name='available_from_time',
        ),
        migrations.RenameField(
            model_name='abstractentrancestep',
            old_name='available_to_time_key_date',
            new_name='available_to_time',
        ),
    ]
