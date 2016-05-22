from django.db import models

import school.models
import user.models


class EnrolledScanRequirement(models.Model):
    for_school = models.ForeignKey(school.models.School)

    short_name = models.CharField(max_length=100, help_text='Используется в урлах. Лучше обойтись маленькими буквами, цифрами и подчёркиванием')

    name = models.TextField(help_text='Например, «Квитанция об оплате»')

    name_genitive = models.TextField(help_text='Например, «квитанцию об оплате»')

    def __str__(self):
        return '%s. Скан «%s»' % (self.for_school, self.name)

    class Meta:
        unique_together = ('for_school', 'short_name')


class EnrolledScan(models.Model):
    requirement = models.ForeignKey(EnrolledScanRequirement)

    for_user = models.ForeignKey(user.models.User)

    original_filename = models.TextField()

    filename = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )
