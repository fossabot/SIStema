# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0012_auto_20160328_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrancelevelrequirement',
            name='questionnaire',
            field=models.ForeignKey(default=None, to='topics.TopicQuestionnaire'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='entrancelevelrequirement',
            unique_together=set([('questionnaire', 'entrance_level', 'tag')]),
        ),
    ]
