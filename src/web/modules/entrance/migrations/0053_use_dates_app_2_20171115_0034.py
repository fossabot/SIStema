# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def make_key_dates(apps, _schema_editor):
    AbstractEntranceStep = apps.get_model('entrance', 'AbstractEntranceStep')
    KeyDate = apps.get_model('dates', 'KeyDate')

    # artemtab: As I understand it, we don't have usual polymorphic behavior
    # here, because django restores historical model classes from db data
    # instead of using the original model class.
    # Though, it shouldn't be the problem for us, because we only want to
    # modify fields on the original AbstractEntranceStep table.
    for step in AbstractEntranceStep.objects.all():
        if step.available_from_time is not None:
            # Using (school, order) pair as step identifier as we don't have
            # the original __str__ method here
            step.available_from_time_key_date = KeyDate.objects.create(
                datetime=step.available_from_time,
                name='Начало для шага "{}: {}"'.format(step.school.name,
                                                       step.order),
            )
            step.save()

        if step.available_to_time is not None:
            # Using (school, order) pair as step identifier as we don't have
            # the original __str__ method here
            step.available_to_time_key_date = KeyDate.objects.create(
                datetime=step.available_to_time,
                name='Дедлайн для шага "{}: {}"'.format(step.school.name,
                                                        step.order),
            )
            step.save()


def make_key_dates_reverse(apps, _schema_editor):
    AbstractEntranceStep = apps.get_model('entrance', 'AbstractEntranceStep')

    # artemtab: As I understand it, we don't have usual polymorphic behavior
    # here, because django restores historical model classes from db data
    # instead of using the original model class.
    # Though, it shouldn't be the problem for us, because we only want to
    # modify fields on the original AbstractEntranceStep table.
    for step in AbstractEntranceStep.objects.all():
        if step.available_from_time_key_date is not None:
            step.available_from_time = (
                step.available_from_time_key_date.datetime)
            step.save()

        if step.available_to_time_key_date is not None:
            step.available_to_time = step.available_to_time_key_date.datetime
            step.save()


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0052_use_dates_app_1_20171115_0034'),
    ]

    operations = [
        migrations.RunPython(
            code=make_key_dates,
            reverse_code=make_key_dates_reverse,
        ),
    ]
