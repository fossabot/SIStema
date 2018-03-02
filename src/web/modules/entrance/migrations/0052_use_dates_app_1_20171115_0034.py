# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dates', '0001_initial'),
        ('entrance', '0051_userparticipatedinschoolentrancestepexception'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractentrancestep',
            name='available_from_time_key_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dates.KeyDate', verbose_name='Доступен с'),
        ),
        migrations.AddField(
            model_name='abstractentrancestep',
            name='available_to_time_key_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='dates.KeyDate', verbose_name='Доступен до'),
        ),
    ]
