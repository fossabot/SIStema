# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modules.entrance.models


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0010_auto_20160424_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkinglock',
            name='locked_until',
            field=models.DateTimeField(default=modules.entrance.models.get_locked_timeout),
        ),
    ]
