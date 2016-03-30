# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0010_entrancestep'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrancestep',
            name='params',
            field=models.TextField(default=(), help_text='Параметры для шага'),
            preserve_default=False,
        ),
    ]
