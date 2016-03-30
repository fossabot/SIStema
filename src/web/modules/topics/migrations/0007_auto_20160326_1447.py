# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0006_auto_20160326_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scale',
            old_name='values_count',
            new_name='count_values',
        ),
    ]
