#!/usr/bin/env python
"""Staging version of settings.

USAGE:
  python manage.py runserver --settings=setting.staging_settings

Here we inherit from base settings and just override staging specific items.
"""

import db_config 

from base_settings import *
from settings.keys import keys


ENVIRON = ENV_STAGING

DEBUG = True 
TEMPLATE_DEBUG = True

# ADMINS = (
#      ('bugs', ''),
# )

STATIC_ROOT = os.path.join(ROOT_PATH, '../../static_app/')

DATABASES['default'].update(db_config.DEFAULT_STAGING_DATABASE_CONFIG)
DATABASES['readonly'].update(db_config.READONLY_STAGING_DATABASE_CONFIG)

ROOT_URL = '100.cst.co.in/'
ROOT_URL_WITH_SCHEME = 'http://' + ROOT_URL

ALLOWED_HOSTS = [
    # UI
    '100.cst.co.in',
    'www.100.cst.co.in',
    # API
    '100.api.cst.com',
    'www.100.api.cst.com',
    '100.api.cst.co.in',
    'www.100.api.cst.co.in',
    # LOCAL
    'localhost',
]

WSGI_APPLICATION = 'wsgi.staging.application' 

SESSION_COOKIE_DOMAIN = '.100.cst.com'

CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'DELETE',
)
#--------------- / end / -----------------


######################################################################################
## social Media IDS ##
######################################################################################

# Instagram
INSTAGRAM_CLIENT_ID = keys.INSTAGRAM_CLIENT_ID_STAGING
INSTAGRAM_CLIENT_SECRET = keys.INSTAGRAM_CLIENT_SECRET_STAGING

# Facebook
FACEBOOK_CLIENT_ID = keys.FACEBOOK_CLIENT_ID_STAGING
FACEBOOK_CLIENT_SECRET = keys.FACEBOOK_CLIENT_SECRET_STAGING

######################################################################################