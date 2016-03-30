# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0010_auto_20160327_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestionnairestatus',
            name='questionnaire',
            field=models.ForeignKey(related_name='+', to='topics.TopicQuestionnaire'),
        ),
        migrations.AlterField(
            model_name='userquestionnairestatus',
            name='user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
