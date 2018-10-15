"""Lo usa ./cron/ping_google y hace un ping a google :)"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.prod')

import django
django.setup()

from django.contrib.sitemaps import ping_google

try:
    ping_google()
    print('Ping a google con exito')
except:
    print('Error al hacer ping en google')
