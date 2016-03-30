# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0008_auto_20160324_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entranceexam',
            name='for_school',
            field=models.OneToOneField(to='school.School'),
        ),
    ]
