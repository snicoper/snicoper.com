# flake8: noqa
from .base import *

INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.100']

# Application definition
THIRD_PARTY_APPS += (
    'debug_toolbar',
    'django_extensions',
)

LOCAL_APPS += ()

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/local')

# Emails
DEFAULT_FROM_EMAIL = 'snicoper@snicoper.local'

# Admins
ADMINS = (
    ('snicoper', 'snicoper@snicoper.local'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'snicoperdev',
        'USER': 'snicoper',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Grupos de email.
GROUP_EMAILS = {
    "NO-REPLY": 'no-responder@snicoper.local <snicoper@snicoper.local>',
    'CONTACTS': (
        'Salvador Nicolas <snicoper@snicoper.local>',
    )
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ¿Mostrar fake adsense? muestra unas imágenes en su lugar.
ADSENSE_IMAGES_FAKE = False
