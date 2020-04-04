from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.timezone import now

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
        'get_ssl_expiry_date',
    )
    search_fields = ('name', 'url',)

    fields = ('name', 'url', 'active')

    def get_ssl_expiry_date(self, instance):
        if not instance.ssl_expiry_date:
            return '-'

        delta = instance.ssl_expiry_date - now().date()
        if delta.days <= 0:
            return mark_safe('<span style="color:red">nieważny od {} dni</span>'.format(delta.days))

        if delta.days <= 14:
            return mark_safe('<span style="color:orange">wygasa za {} dni</span>'.format(delta.days))

        return instance.ssl_expiry_date

    get_ssl_expiry_date.short_description = 'Ważność certyfikatu'


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
