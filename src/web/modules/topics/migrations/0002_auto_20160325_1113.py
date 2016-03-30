# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leveldownwarddependency',
            options={'verbose_name_plural': 'Level downward dependencies'},
        ),
        migrations.AlterModelOptions(
            name='levelupwarddependency',
            options={'verbose_name_plural': 'Level upward dependencies'},
        ),
        migrations.AlterModelOptions(
            name='topicdependency',
            options={'verbose_name_plural': 'Topic dependencies'},
        ),
        migrations.AddField(
            model_name='scalelabel',
            name='mark',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('questionnaire', 'short_name')]),
        ),
    ]
