from django.contrib import admin


class AbstractHomePageBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'order')
    list_filter = ('school', )
