#!/usr/bin/env python
# flake8: noqa

# Para pruebas rápidas

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.local')

import django
django.setup()

##############################################################################
