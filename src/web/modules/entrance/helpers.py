from . import models


def get_enrolling_users_ids(school):
    return models.EntranceStatus.objects.filter(
        school=school
    ).exclude(
        status=models.EntranceStatus.Status.NOT_PARTICIPATED
    ).values_list('user_id', flat=True)
