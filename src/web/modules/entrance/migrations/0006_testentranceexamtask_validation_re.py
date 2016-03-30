# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0005_auto_20160320_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='testentranceexamtask',
            name='validation_re',
            field=models.CharField(blank=True, help_text='Регулярное выражение для валидации ввода', max_length=100),
        ),
    ]
