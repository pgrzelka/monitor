import json
from datetime import datetime
from time import time

import requests
import ssl, socket

from django.core.management import BaseCommand
from django.utils.dateparse import parse_datetime
from dateutil.parser import parse

from website.models import Website, Check

get_ms = lambda: int(round(time() * 1000))


class Command(BaseCommand):

    def handle(self, *args, **options):
        model = Website.objects.filter(last_check__isnull=True).first()
        if not model:
            model = Website.objects.order_by('last_check').first()

        check = Check(website=model)

        hostname = model.url.replace('https://', '').replace('http://', '')

        print("Checking: {} / {}".format(model.name, hostname))

        try:
            context = ssl.create_default_context()

            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    data = ssock.getpeercert()
                    check.ssl_expiry_date = parse(data['notAfter'])
        except:
            pass

        ms = get_ms()
        try:
            r = requests.get(model.url)

            check.hsts_header = 'Strict-Transport-Security' in r.headers.keys()
            check.http_status = r.status_code
        except:
            pass

        check.delay = (get_ms() - ms) / 1000

        check.save()
