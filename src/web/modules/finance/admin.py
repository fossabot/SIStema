from django.contrib import admin

from . import models
import questionnaire.admin


class PaymentAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'for_user', 'amount')
    list_filter = ('for_school',)
    search_fields = ('for_user__first_name', 'for_user__last_name', 'for_user__username')

admin.site.register(models.PaymentAmount, PaymentAmountAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'for_user', 'type', 'amount', 'private_comment',
                    'public_comment')
    list_filter = ('for_school', 'type')
    search_fields = ('for_user__first_name', 'for_user__last_name', 'for_user__username',
                     'private_comment', 'public_comment')

admin.site.register(models.Discount, DiscountAdmin)


admin.site.register(models.PaymentInfoQuestionnaireBlock,
                    questionnaire.admin.AbstractQuestionnaireBlockAdmin)
