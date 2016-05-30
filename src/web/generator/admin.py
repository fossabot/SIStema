from django.contrib import admin

from . import models


class FontAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'filename')
    search_fields = ('name', )
    list_display_links = ('id', 'name')

admin.site.register(models.Font, FontAdmin)


class FontFamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'normal', 'bold', 'italic', 'bold_italic')
    search_fields = ('name', )
    list_display_links = ('id', 'name')

admin.site.register(models.FontFamily, FontFamilyAdmin)


class ParagraphStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'leading', 'alignment', 'font', 'font_size', 'bullet_font',
                    'space_before', 'space_after', 'left_indent')
    search_fields = ('name', )

admin.site.register(models.ParagraphStyle, ParagraphStyleAdmin)


class FontTableStyleCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'start', 'stop', 'font', 'size')
    list_filter = ('table', 'font')

admin.site.register(models.FontTableStyleCommand, FontTableStyleCommandAdmin)


class LeadingTableStyleCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'start', 'stop', 'leading')
    list_filter = ('table', )

admin.site.register(models.LeadingTableStyleCommand, LeadingTableStyleCommandAdmin)


class TextColorTableStyleCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'start', 'stop', 'color')
    list_filter = ('table', )

admin.site.register(models.TextColorTableStyleCommand, TextColorTableStyleCommandAdmin)


class AlignmentTableStyleCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'start', 'stop', 'align')
    list_filter = ('table', )

admin.site.register(models.AlignmentTableStyleCommand, AlignmentTableStyleCommandAdmin)


class PaddingTableStyleCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'start', 'stop', 'direction', 'padding')
    list_filter = ('table', )

admin.site.register(models.PaddingTableStyleCommand, PaddingTableStyleCommandAdmin)


class ValignTableStyleCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'start', 'stop', 'direction')
    list_filter = ('table', )

admin.site.register(models.ValignTableStyleCommand, ValignTableStyleCommandAdmin)


class LineTableStyleCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'start', 'stop', 'command_name', 'thickness', 'color')
    list_filter = ('table', 'command_name')

admin.site.register(models.LineTableStyleCommand, LineTableStyleCommandAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'page_size')

admin.site.register(models.Document, DocumentAdmin)


class AbstractDocumentBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'order')
    list_filter = (('document', admin.RelatedOnlyFieldListFilter), )
    ordering = ('document', 'order')


admin.site.register(models.Paragraph, AbstractDocumentBlockAdmin)
admin.site.register(models.PageBreak, AbstractDocumentBlockAdmin)
admin.site.register(models.Spacer, AbstractDocumentBlockAdmin)
admin.site.register(models.Table, AbstractDocumentBlockAdmin)


class TableRowAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'order')
    list_filter = ('table', )
    ordering = ('table', 'order')

admin.site.register(models.TableRow, TableRowAdmin)


class TableCellAdmin(admin.ModelAdmin):
    list_display = ('id', 'row', 'order')
    list_filter = ('row__table', 'row',)
    ordering = ('row__table', 'row', 'order')


admin.site.register(models.TableCell, TableCellAdmin)
