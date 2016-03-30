# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='programentranceexamtask',
            name='input_file_name',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programentranceexamtask',
            name='input_format',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programentranceexamtask',
            name='memory_limit',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programentranceexamtask',
            name='output_file_name',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programentranceexamtask',
            name='output_format',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programentranceexamtask',
            name='time_limit',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
