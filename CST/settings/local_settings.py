"""Local version of settings.

USAGE:
  python manage.py runserver --settings=setting.local_settings

Here we inherit from test settings and just override local specific items.
"""
import os
import logging

import db_config 
from base_settings import *


ENVIRON = ENV_LOCAL

TEST_WITHOUT_MIGRATIONS_COMMAND = 'django_nose.management.commands.test.Command'

DEBUG = True
TASTYPIE_FULL_DEBUG = True
TEMPLATE_DEBUG = True

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}

DATABASES['default'].update(db_config.DEFAULT_LOCAL_DATABASE_CONFIG)
DATABASES['readonly'].update(db_config.READONLY_LOCAL_DATABASE_CONFIG)
DATABASES['staging'] = db_config.DEFAULT_LOCAL_DATABASE_CONFIG
# We use the same database as LOCAL_STAGING as it is only for testing purpose
DATABASES['prod'] = db_config.DEFAULT_LOCAL_DATABASE_CONFIG

#--------------- CACHING -----------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-bar'
    },
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'lm'
    }
}
#-------------- / end / ------------------

ROOT_URL = 'localhost:8000/'
ROOT_URL_WITH_SCHEME = 'http://' + ROOT_URL

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
    'debug_toolbar',
)

CORS_ORIGIN_WHITELIST += ()

WSGI_APPLICATION = 'wsgi.local.application'

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    logging.disable(logging.WARNING)

RUNNING_TESTS = True
