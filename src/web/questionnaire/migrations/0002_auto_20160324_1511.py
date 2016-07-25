# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='for_school',
            field=models.ForeignKey(to='schools.School', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='for_session',
            field=models.ForeignKey(to='schools.Session', null=True, blank=True),
        ),
    ]
