# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0009_topicissue_is_correcting'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackupUserMark',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('mark', models.PositiveIntegerField()),
                ('is_automatically', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('scale_in_topic', models.ForeignKey(to='topics.ScaleInTopic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='backupusermark',
            unique_together=set([('user', 'scale_in_topic')]),
        ),
    ]
