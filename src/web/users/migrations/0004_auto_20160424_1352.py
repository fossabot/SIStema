# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160419_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
    ]
