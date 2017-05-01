from groups import models


def is_user_in_group(user, school, group_name):
    group = models.Group.objects.filter(
        school=school, short_name=group_name
    ).first()
    if group is None:
        raise ValueError('Unknown group name %s for school %s' % (
            group_name,
            school
        ))

    return group.is_user_in_group(user)
