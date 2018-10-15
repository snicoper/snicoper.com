# flake8: noqa
from .base import *

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ['127.0.0.1']

# Application definition
THIRD_PARTY_APPS += ()

LOCAL_APPS += ()

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_django_db',
        'USER': 'test_django',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/test')

# Emails
DEFAULT_FROM_EMAIL = 'snicoper@snicoper.local'

# Admins
ADMINS = (
    ('snicoper', 'snicoper@snicoper.local'),
)

# Grupos de email.
GROUP_EMAILS = {
    "NO-REPLY": 'no-responder@snicoper.local <snicoper@snicoper.local>',
    'CONTACTS': (
        'Salvador Nicolas <snicoper@snicoper.local>',
    ),
}
