# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20160320_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='full_name',
            field=models.TextField(help_text='Полное название, не аббревиатура. По умолчанию совпадает с обычным названием. Например, «Летняя компьютерная школа 2015»', default=''),
            preserve_default=False,
        ),
    ]
