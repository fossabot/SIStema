from django.contrib import admin

from . import models
import questionnaire.admin


class PaymentAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'for_user', 'amount')
    list_filter = ('for_school',)
    search_fields = ('for_user__first_name', 'for_user__last_name', 'for_user__username')

admin.site.register(models.PaymentAmount, PaymentAmountAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_school', 'for_user', 'type', 'amount', 'private_comment', 'public_comment')
    list_filter = ('for_school', 'type')
    search_fields = ('for_user__first_name', 'for_user__last_name', 'for_user__username', 'private_comment', 'public_comment')

admin.site.register(models.Discount, DiscountAdmin)


admin.site.register(models.PaymentInfoQuestionnaireBlock, questionnaire.admin.AbstractQuestionnaireBlockAdmin)


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
