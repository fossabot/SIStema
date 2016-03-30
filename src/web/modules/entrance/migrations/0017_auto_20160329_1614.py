# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0016_auto_20160329_1251'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='entranceexamtasksolution',
            index_together=set([('task', 'user')]),
        ),
    ]
