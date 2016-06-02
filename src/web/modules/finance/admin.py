from django.contrib import admin

from . import models
import questionnaire.admin
import user.models
import modules.entrance.models


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

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'for_user':
            kwargs['queryset'] = (
                user.models.User.objects.filter(
                    entrance_statuses__status=modules.entrance.models.EntranceStatus.Status.ENROLLED
                ).order_by('last_name', 'first_name'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.Discount, DiscountAdmin)


admin.site.register(models.PaymentInfoQuestionnaireBlock,
                    questionnaire.admin.AbstractQuestionnaireBlockAdmin)


class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'short_name', 'name')
    list_display_links = ('id', 'short_name')
    search_fields = ('short_name', 'name')
    list_filter = ('for_school', )

admin.site.register(models.DocumentType, DocumentTypeAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'type', '_users_list', 'created_at')
    search_fields = ('for_users__first_name', 'for_users__last_name', 'for_users__email')
    list_filter = ('for_school', 'type')

admin.site.register(models.Document, DocumentAdmin)


class QuestionnaireVariantDocumentGenerationConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'variant', 'document_type')
    list_filter = ('document_type', )

admin.site.register(models.QuestionnaireVariantDocumentGenerationCondition,
                    QuestionnaireVariantDocumentGenerationConditionAdmin)
