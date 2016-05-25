# -*- coding: utf-8 -*-

from django.db import models

from .discount import Discount

import school.models
import user.models


class PaymentAmount(models.Model):
    for_school = models.ForeignKey(school.models.School, related_name='+')

    for_user = models.ForeignKey(user.models.User, related_name='+')

    amount = models.PositiveIntegerField(help_text='Сумма к оплате')

    class Meta:
        unique_together = ('for_school', 'for_user')

    @classmethod
    def get_amount_for_user(cls, school, user):
        amount = cls.objects.filter(for_school=school, for_user=user).first()
        if amount is None:
            return None
        amount = amount.amount

        discounts = (Discount.objects
                             .filter(for_school=school, for_user=user)
                             .values_list('amount', flat=True))

        max_discount = max(discounts, default=0)

        amount -= max_discount
        if amount < 0:
            amount = 0

        return amount
