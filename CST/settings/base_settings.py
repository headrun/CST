#!/usr/bin/env python
"""
Django settings for CST project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import datetime
import djcelery
import os
import pytz
import sys

from datetime import date
from django.utils import timezone
from os.path import abspath, dirname, basename, join


djcelery.setup_loader()
sys.path.append(os.getcwd())

ROOT_PATH = abspath(join(dirname(__file__), '..'))
PROJECT_NAME = basename(abspath(dirname(__file__)))

TEMPLATE_DIRS = (join(ROOT_PATH, 'templates'),)

ENV_LOCAL = 'local'
ENV_STAGING = 'staging'
ENV_PROD = 'prod'

ENVIRON = ENV_LOCAL

API_THROTTLE_RATE = 500

# No slash is needed at the end of API call.
TASTYPIE_ALLOW_MISSING_SLASH = True

USE_TZ = True

# ADMINS = (
#     ('admin', ''),
# )

# MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Sqlite3 so that tests to run blazingly fast!
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/dev/shm/sqlite3.db',
        'TEST_CHARSET': 'UTF8',
        'TEST_NAME': None  # in-memory sqlite db
    },
    'readonly': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/dev/shm/sqlite3.db',
        'TEST_CHARSET': 'UTF8',
        'TEST_NAME': None  # in-memory sqlite db
    },
    'staging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/dev/shm/sqlite3_staging.db',
        'TEST_CHARSET': 'UTF8',
        'TEST_NAME': None  # in-memory sqlite db
    },
    'prod': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/dev/shm/sqlite3_prod.db',
        'TEST_CHARSET': 'UTF8',
        'TEST_NAME': None  # in-memory sqlite db
    }
}


#----------------/ CELERY /-----------------/
CELERY_EMAIL_TASK_CONFIG = {}

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND="redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
#----------------/ END /-----------------/


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Calcutta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT_PATH, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
)

# List of finder classes +that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xf_4a43y!&_u@4w**xwox5^^m96%06q@y!r))ng)*&_$dtu-8%'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django_mobile.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'corsheaders.middleware.CorsMiddleware',            # CORS
    'cst.middleware.CsrfCookieMiddleware',           # CSRF for views
    'cst.middleware.TimezoneMiddleware',             # get user tz 
    'cst.middleware.RemoteUserMiddleware',           # remote user username and id 
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.template.context_processors.request',
    'django_mobile.context_processors.flavour',
    # 'allauth.account.context_processors.account',
    # 'allauth.socialaccount.context_processors.socialaccount',
    'cst.utils.settings_environment',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',                # Needed to login by username in Django admin, regardless of 'allauth'
    'allauth.account.auth_backends.AuthenticationBackend',      # 'allauth' specific authentication methods, such as login by e-mail
    'cst.auth_backends.ApiKeyAuthBackend',                   # Needed to login by username and apikey
]

ROOT_URLCONF = 'cst.urls'

# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (join(ROOT_PATH, 'templates'),)

OVERRIDE_APPS = [
    'test_without_migrations',
]

DJANGO_APPPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.instagram',
    'bootstrapform',
    'corsheaders',
    'djangobower',
    'django_nose',
    'djcelery',
    'djcelery_email',
    'djsupervisor',
    'djrill',
    'kombu',
    'longerusername',
    'tastypie',
]

CUSTOM_APPS = [
    'accounts',
    'common_exceptions',
    'crawlers',
    'projects',
    'test_views',
]

INSTALLED_APPS = OVERRIDE_APPS + DJANGO_APPPS + THIRD_PARTY_APPS + CUSTOM_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(process)d %(thread)d %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
         },
        'suppress_unreadable_post': {
            '()': 'cst.logging_utils.SuppressUnreadablePost',
        },
        'suppress_suspicious_operation': {
            '()': 'cst.logging_utils.SuppressSuspiciousOperation',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'requests.log',
            'maxBytes': 1024 * 32,
            'backupCount': 3
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': [
                'require_debug_false',
                'suppress_unreadable_post',
                'suppress_suspicious_operation'
            ],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'request.logger': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

#------------ CORS WHILIST DOMAINS -----------------#
CORS_ORIGIN_WHITELIST = (
    'localhost',
)

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'DELETE',
)

INTERNAL_IPS = ('127.0.0.1',)

#--------------- / end / -----------------#

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

RAMDISK_SIZE = 200  # default to 128 MB. override with -s option
RAMDISK_PATH = '/dev/disk1'  # overide with -p option


#--------------- CACHING -----------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}
#--------------- / end / -----------------

CACHE_VERSION = 1

RUNNING_TESTS = False

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


ROOT_URL = 'localhost:8000/'
ROOT_URL_WITH_SCHEME = 'http://' + ROOT_URL


CONN_MAX_AGE = 3600
TEST_WITHOUT_MIGRATIONS_COMMAND = 'django_nose.management.commands.test.Command'

# if X-Forwarded-Proto(set by ELB) is https then treat this connection as secure
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TASTYPIE_DEFAULT_FORMATS = ['json']

## ------------ Bower Components ---------- ##
BOWER_COMPONENTS_ROOT = os.path.join(ROOT_PATH, 'bower_files')
BOWER_INSTALLED_APPS = (
    'app-datepicker',
    'app-layout',
    'GoogleWebComponents/google-chart#^1.0.0',
    'GoogleWebComponents/firebase-element#^1.0.15',
    'iron-swipeable-pages#^1.0.7',
    'jquery#1.9',
    'jv-datepicker',
    'moment',
    'neon-animation',
    'paper-autocomplete#1.1.1',
    'paper-datatable',
    'paper-date-picker',
    'paper-fab#^1.2.0',
    'paper-input-autocomplete-chips',
    'paper-search#^1.0.22',
    'paper-time-picker',
    'paper-toast#1.2.2',
    'progressbar.js#^1.0.0',
    'Polymer/polymer#^1.4.0',
    'PolymerElements/app-layout#^0.9.0',
    'polymerelements/app-route#^0.9.1',
    'PolymerElements/iron-elements#^1.0.0',
    'PolymerElements/neon-elements#^1.0.0',
    'PolymerElements/paper-elements#^1.0.1',
    'PolymerElements/platinum-elements#^1.1.0',
    'social-media-icons',
    'vaadin-combo-box',
    'visionmedia/page.js#~1.6.4'
)

## ---------------------------------------------------- ##


SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email','public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'kr_KR',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'
    }
}

ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_USERNAME_REQURIED=True

LOGIN_REDIRECT_URL = '/test/test'

SOCIALACCOUNT_QUERY_EMAIL = True
