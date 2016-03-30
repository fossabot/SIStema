# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0012_entrancelevel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrancelevel',
            options={'ordering': ['for_school_id', 'order']},
        ),
        migrations.AddField(
            model_name='entrancelevel',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
