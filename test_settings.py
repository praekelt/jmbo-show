# We're still on Django 1.4 and use django-setuptest. Use this as a starting
# point for your test settings. Typically copy this file as test_settings.py
# and replace myapp with your app name.
from os.path import expanduser

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jmbo',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

FOUNDRY = {
    'sms_gateway_api_key': '',
    'sms_gateway_password': '',
    'layers': ('basic',)
}

INSTALLED_APPS = (
    'show',
    'foundry',
    'jmbo',
    'photologue',
    'jmbo_calendar',
    'category',
    'likes',
    'secretballot',
    'publisher',
    'preferences',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sites'
)

ROOT_URLCONF = 'show.urls'

USE_TZ = True
TIME_ZONE = 'GMT'

SITE_ID = 1

STATIC_URL = '/static/'

CKEDITOR_UPLOAD_PATH = expanduser('~')

SOUTH_TESTS_MIGRATE = False

# Disable celery
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'
