# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ejudge', '0004_auto_20160329_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutioncheckingresult',
            name='failed_test',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]
