# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_school_full_name'),
        ('entrance', '0009_auto_20160327_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('class_name', models.CharField(max_length=100, help_text='Путь до класса, описывающий шаг')),
                ('order', models.IntegerField()),
                ('for_school', models.ForeignKey(to='school.School', related_name='entrance_steps')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
