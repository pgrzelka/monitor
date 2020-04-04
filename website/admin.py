from django.contrib import admin

from website.models import Website, Check


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'url',
        'last_online',
        'last_check',
        'http_status',
        'hsts_header',
        'delay',
        'delay_avg',
        'ssl_expiry_date',
    )
    search_fields = ('name', 'url',)

    fields = ('name', 'url', 'active')


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = (
        'website',
        'http_status',
        'hsts_header',
        'delay',
        'ssl_expiry_date',
        'date_created',
    )
    list_filter = ('website',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
