# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0002_auto_20160330_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programentranceexamtask',
            name='input_file_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='programentranceexamtask',
            name='input_format',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='programentranceexamtask',
            name='output_file_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='programentranceexamtask',
            name='output_format',
            field=models.TextField(blank=True),
        ),
    ]
