# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0015_auto_20160508_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='userincheckinggroup',
            name='is_actual',
            field=models.BooleanField(default=True),
        ),
    ]
