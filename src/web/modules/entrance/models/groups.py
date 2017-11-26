from django.db import models

import groups.models
from .main import EntranceStatus


class EntranceStatusGroup(groups.models.AbstractGroup):
    status = models.IntegerField(
        choices=EntranceStatus.Status.choices,
        validators=[EntranceStatus.Status.validator]
    )

    def is_user_in_group(self, user):
        EntranceStatus.objects.filter(
            user=user,
            status=self.status,
            school=self.school,
        )
