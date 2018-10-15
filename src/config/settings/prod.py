# flake8: noqa
from .base import *

SECRET_KEY = '+hi+cb#ij4n)*^kci&53^_=ujq04q31fl^at7#=3*i-j85(_v+'

DEBUG = False

ALLOWED_HOSTS = ['.snicoper.com']

# Sessions
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_DOMAIN = '.snicoper.com'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Application definition
THIRD_PARTY_APPS += ()

LOCAL_APPS += ()

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# TEMPLATE CONFIGURATION
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/prod')

# Emails
DEFAULT_FROM_EMAIL = 'snicoper@snicoper.com'

# Admins
ADMINS = (
    ('snicoper', 'snicoper@snicoper.com'),
)

# Grupos de email.
GROUP_EMAILS = {
    'NO-REPLY': 'no-responder@snicoper.com <snicoper@snicoper.com>',
    'CONTACTS': (
        'Salvador Nicolas <snicoper@snicoper.com>',
    )
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'snicopercom',
        'USER': 'snicopercom',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Configuración smtp.
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.snicoper.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'snicoper'
EMAIL_HOST_PASSWORD = ''

# haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'whoosh_index'),
    }
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Disqus
DISQUS_SHORTNAME = 'snicoper-com'
