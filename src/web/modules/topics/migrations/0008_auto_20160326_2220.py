# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0007_auto_20160326_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermark',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 26, 17, 20, 48, 599518, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='leveldownwarddependency',
            name='destination_level',
            field=models.ForeignKey(to='topics.Level', related_name='+'),
        ),
        migrations.AlterField(
            model_name='leveldownwarddependency',
            name='min_percent',
            field=models.IntegerField(help_text='Минимальный процент максимальных/минимальных оценок из source_level', validators=[django.core.validators.MinValueValidator(0, message='Процент не может быть меньше нуля'), django.core.validators.MaxValueValidator(100, message='Процент не может быть больше 100')]),
        ),
        migrations.AlterField(
            model_name='leveldownwarddependency',
            name='source_level',
            field=models.ForeignKey(to='topics.Level', related_name='+'),
        ),
        migrations.AlterField(
            model_name='levelupwarddependency',
            name='destination_level',
            field=models.ForeignKey(to='topics.Level', related_name='+'),
        ),
        migrations.AlterField(
            model_name='levelupwarddependency',
            name='min_percent',
            field=models.IntegerField(help_text='Минимальный процент максимальных/минимальных оценок из source_level', validators=[django.core.validators.MinValueValidator(0, message='Процент не может быть меньше нуля'), django.core.validators.MaxValueValidator(100, message='Процент не может быть больше 100')]),
        ),
        migrations.AlterField(
            model_name='levelupwarddependency',
            name='source_level',
            field=models.ForeignKey(to='topics.Level', related_name='+'),
        ),
        migrations.AlterField(
            model_name='scale',
            name='title',
            field=models.CharField(help_text='Например, «Практика». Показывается школьнику', max_length=100),
        ),
        migrations.AlterField(
            model_name='usermark',
            name='is_automatically',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='leveldownwarddependency',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='levelupwarddependency',
            unique_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='topicdependency',
            index_together=set([('source', 'destination'), ('source', 'source_mark')]),
        ),
    ]
