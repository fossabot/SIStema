# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ejudge', '0006_auto_20160329_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutioncheckingresult',
            name='memory_consumed',
            field=models.PositiveIntegerField(help_text='В байтах', default=0),
        ),
        migrations.AlterField(
            model_name='testcheckingresult',
            name='memory_consumed',
            field=models.PositiveIntegerField(help_text='В байтах', default=0),
        ),
    ]
