# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
APPS_DIR = os.path.join(BASE_DIR, 'apps')

# Add BASE_DIR and APPS_DIR to $PYTHONPATH.
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, APPS_DIR)

DEBUG = True

SECRET_KEY = 'bbh%5#!h1tdoz2a1b&#mb8!&nebshil-+ai-vxqwt@72)*ohok'

# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
)

THIRD_PARTY_APPS = (
    'haystack',
    'rest_framework',
)

LOCAL_APPS = (
    'accounts.apps.AccountsConfig',
    'authentication.apps.AuthenticationConfig',
    'blog.apps.BlogConfig',
    'contact.apps.ContactConfig',
    'djtemplateforms.apps.DjtemplateformsConfig',
    'home.apps.HomeConfig',
    'pages.apps.PagesConfig',
    'search.apps.SearchConfig',
    'stats.apps.StatsConfig',
    'utils.apps.UtilsConfig',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.common_template_vars',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Site
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Media
MEDIA_URL = '/media/'

# Users
AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/auth/login/'

AUTHENTICATION_BACKENDS = (
    'authentication.backends.EmailOrUsernameModelBackend',
)

# Fixtures para desarrollo y tests
FIXTURE_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), 'fixtures'),
)

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# DRF 287
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
}
