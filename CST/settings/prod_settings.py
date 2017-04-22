#!/usr/bin/env python
"""Production version of settings.

USAGE:
  python manage.py runserver --settings=setting.prod_settings

Here we inherit from dev settings and just override prod specific items.
"""


import db_config 

from base_settings import *
from settings.keys import keys


ENVIRON = ENV_PROD

DEBUG = False
TEMPLATE_DEBUG = False

# ADMINS = (
#      ('prod_bugs', ''),
# )

STATIC_ROOT = os.path.join(ROOT_PATH, '../../static_app/')

DATABASES['default'].update(db_config.DEFAULT_PROD_DATABASE_CONFIG)
DATABASES['readonly'].update(db_config.READONLY_PROD_DATABASE_CONFIG)

ROOT_URL = 'beta.cst.co.in/'
ROOT_URL_WITH_SCHEME = 'http://' + ROOT_URL

ALLOWED_HOSTS = [
    # UI
    'cst.com',
    'www.cst.com',
    'beta.cst.co.in',
    'www.beta.cst.co.in',
    # API
    'api.cst.com',
    'www.api.cst.com',
    'api.cst.co.in',
    'www.api.cst.co.in',
    # LOCAL
    'localhost',
]

WSGI_APPLICATION = 'wsgi.prod.application'

SESSION_COOKIE_DOMAIN = ".cst.com"

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
INSTAGRAM_CLIENT_ID = keys.INSTAGRAM_CLIENT_ID_PROD
INSTAGRAM_CLIENT_SECRET = keys.INSTAGRAM_CLIENT_SECRET_PROD

# Facebook
FACEBOOK_CLIENT_ID = keys.FACEBOOK_CLIENT_ID_PROD
FACEBOOK_CLIENT_SECRET = keys.FACEBOOK_CLIENT_SECRET_PROD

######################################################################################