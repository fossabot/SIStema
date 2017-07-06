# -*- coding: utf-8 -*-

from django.core.management import base as management_base

from users import models as users_models
from schools import models as schools_models
from modules.topics import models as topics_models


class Command(management_base.BaseCommand):
    help = 'Export table with topics answers'

    def add_arguments(self, parser):
        parser.add_argument('--session-id', type=int, help='filter by models.schools.Session.id')
        parser.add_argument('--parallel-id', type=int, help='filter by models.schools.Parallel.id')

    def handle(self, *args, **options):
        queryset = users_models.User.objects
        session = schools_models.Session.objects.filter(id=options['session_id']).first()
        queryset = queryset.filter(entrance_statuses__session_id=session.id)
        if options['parallel_id']:
            queryset = queryset.filter(entrance_statuses__parallel_id=options['parallel_id'])

        users = list(queryset.all())
        user_ids = [user.id for user in users]
        marks = list(topics_models.UserMark.objects
                     .filter(user_id__in=user_ids,
                             scale_in_topic__topic__questionnaire__school_id=session.school_id)
                     .all())
        for mark in marks:
            print('\t'.join((mark.user.get_full_name(),
                             mark.scale_in_topic.topic.short_name,
                             mark.scale_in_topic.topic.text,
                             str(mark.mark),
                             str(mark.is_automatically))))
