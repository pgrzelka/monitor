from django.db import models
from django.utils.translation import gettext_lazy as _


class Website(models.Model):
    name = models.CharField(_("Nazwa"), max_length=100)
    url = models.URLField(_("Url"))

    # search_query = models.CharField(_("Wyszukiwane wyrażenie"), null=True, blank=True)

    date_created = models.DateTimeField(_("Utworzono"), auto_now_add=True)

    active = models.BooleanField(_("Aktywna"), default=True)

    last_online = models.DateTimeField(_("Ostatnio online"), null=True, blank=True)
    last_check = models.DateTimeField(_("Ostatnio sprawdzana"), null=True, blank=True)
    http_status = models.PositiveIntegerField(_("Status HTTP"), null=True, blank=True)
    hsts_header = models.BooleanField(_("HSTS"), null=True, blank=True)
    delay = models.DecimalField(_("Opóźnienie"), null=True, blank=True, decimal_places=3, max_digits=5)
    delay_avg = models.DecimalField(_("Opóźnienie"), null=True, blank=True, decimal_places=3, max_digits=5)
    ssl_expiry_date = models.DateField(_("Ważność SSL"), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Strona")
        verbose_name_plural = _("Strony")
        ordering = ('name',)


class Check(models.Model):
    website = models.ForeignKey(Website, models.CASCADE)

    date_created = models.DateTimeField(_("Utworzono"), auto_now_add=True)

    http_status = models.PositiveIntegerField(_("Status HTTP"), null=True, blank=True)
    hsts_header = models.BooleanField(_("HSTS"), null=True, blank=True)
    delay = models.DecimalField(_("Opóźnienie"), null=True, blank=True, decimal_places=3, max_digits=5)

    ssl_expiry_date = models.DateField(_("Ważność SSL"), null=True, blank=True)

    class Meta:
        verbose_name = _("Check")
        verbose_name_plural = _("Checks")
        ordering = ('-date_created',)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.website.last_check = self.date_created
        self.website.http_status = self.http_status
        self.website.hsts_header = self.hsts_header
        self.website.delay = self.delay
        self.website.ssl_expiry_date = self.ssl_expiry_date
        if self.http_status == 200:
            self.website.last_online = self.date_created
        self.website.save()


