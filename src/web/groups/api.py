def is_user_in_group(user, group_name, school=None):
    """
    Checks if user in group
    :param user: User object
    :param group_name: group's short_name
    :param school: if school is None, looking for only system-wide group.
    Otherwise looking for this school's groups
    :return: True if user is in group, False otherwise
    """
    from groups import models
    
    group = models.AbstractGroup.objects.filter(
        school=school, short_name=group_name
    ).first()
    if group is None:
        raise ValueError('Unknown group name %s for school %s' % (
            group_name,
            school
        ))

    return group.is_user_in_group(user)
