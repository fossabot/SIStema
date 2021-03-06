# Generated by Django 2.0.3 on 2018-05-19 17:50

from django.db import migrations
from django.db.migrations import RunPython


def extract_sessions_and_parallels_forward(apps, schema_editor):
    EntranceStatus = apps.get_model('entrance', 'EntranceStatus')
    EnrolledToSessionAndParallel = apps.get_model('entrance', 'EnrolledToSessionAndParallel')
    for status in EntranceStatus.objects.all():
        if status.session is None and status.parallel is None:
            continue

        EnrolledToSessionAndParallel.objects.create(
            entrance_status=status,
            session=status.session,
            parallel=status.parallel,
        )


def extract_sessions_and_parallels_backward(apps, schema_editor):
    EnrolledToSessionAndParallel = apps.get_model('entrance', 'EnrolledToSessionAndParallel')
    for session_and_parallel in EnrolledToSessionAndParallel.objects.all():
        status = session_and_parallel.entrance_status
        status.session = session_and_parallel.session
        status.parallel = session_and_parallel.parallel
        status.save()


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0078_enrolledtosessionandparallel'),
    ]

    operations = [
        RunPython(
            extract_sessions_and_parallels_forward,
            extract_sessions_and_parallels_backward
        ),
    ]
