"""
Django settings for isl-ideas project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os

import dj_database_url
from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='',
                       cast=lambda v: [s.strip() for s in v.split(',')])


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'islideas',
    'islideas.ideas',
    'channels',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

INSTALLED_APPS += ('django_rq',)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

ROOT_URLCONF = 'islideas.urls'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG":   {
            "hosts": [config('REDIS_URL', default='redis://localhost:6379/0')],
        },
        "ROUTING": "islideas.routing.channel_routing",
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'islideas.context_processors.ws_host',
            ],
            'debug': config('TEMPLATE_DEBUG', default=DEBUG, cast=bool),
        },
    },
]


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(),
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'public')

# Media

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SSL

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SSLIFY_DISABLE = config('SSLIFY_DISABLE', default=False, cast=bool)

SESSION_COOKIE_HTTPONLY = False

# RQ

RQ_QUEUES = {
    'default': {
        'URL': config('REDIS_URL', default='redis://localhost:6379/1'),
    },
    'high': {
        'URL': config('REDIS_URL', default='redis://localhost:6379/1'),
    },
    'low': {
        'URL': config('REDIS_URL', default='redis://localhost:6379/1'),
    },
}

# Sentry

SENTRY_DSN = config('SENTRY_DSN', default=None)
if SENTRY_DSN:
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }

# Project configuration

AUTHENTICATION_BACKENDS = (
    'pythonisl.backends.ISLAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

WS_HOST = config('WS_HOST')
