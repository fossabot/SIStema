# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_school_full_name'),
        ('entrance', '0011_entrancestep_params'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('short_name', models.CharField(help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием', max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('for_school', models.ForeignKey(to='school.School')),
            ],
        ),
    ]
