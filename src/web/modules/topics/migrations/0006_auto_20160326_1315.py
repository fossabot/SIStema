# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0005_auto_20160325_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScaleInTopicIssue',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('label_group', models.ForeignKey(to='topics.ScaleLabelGroup')),
            ],
        ),
        migrations.CreateModel(
            name='TopicIssue',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='order',
            field=models.IntegerField(default=0, help_text='Внутренний порядок возрастания сложности'),
        ),
        migrations.AddField(
            model_name='usermark',
            name='is_automatically',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic',
            name='text',
            field=models.TextField(help_text='Более подробное описание. Показывается школьнику при заполнении анкеты'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(help_text='Показывается школьнику при заполнении анкеты', max_length=100),
        ),
        migrations.AddField(
            model_name='topicissue',
            name='topic',
            field=models.ForeignKey(to='topics.Topic'),
        ),
        migrations.AddField(
            model_name='topicissue',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scaleintopicissue',
            name='topic_issue',
            field=models.ForeignKey(related_name='scales', to='topics.TopicIssue'),
        ),
    ]
