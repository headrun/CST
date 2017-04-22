#******************************************************************************#
#**** [2017] CST
#**** All Rights Reserved.
#******************************************************************************#


# Prod DB CONFIG
#*******************************************************************************#

DEFAULT_PROD_DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'cst_prod',
    'USER': 'cst',
    'PASSWORD': 'fnycwtwprtywepyrtc',
    'HOST': 'localhost',
    'PORT': '3306',
}

READONLY_PROD_DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'cst_prod',
    'USER': 'cst_readonly',
    'PASSWORD': 'fnycwtwprtywepyrtc',
    'HOST': 'localhost',
    'PORT': '3306',
}


# Staging DB CONFIG
#*******************************************************************************#

DEFAULT_STAGING_DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'cst_staging',
    'USER': 'cststage',
    'PASSWORD': 'pxy9ny5pm34y3o',
    'HOST': 'localhost',
    'PORT': '3306',
}

READONLY_STAGING_DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'cst_staging',
    'USER': 'cststage_readonly',
    'PASSWORD': 'sfasfksfoknognngon',
    'HOST': 'localhost',
    'PORT': '3306',
}


# Local DB CONFIG
#*******************************************************************************#

DEFAULT_LOCAL_DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'cst',
    'USER': 'root',
    'PASSWORD': 'root',
    'HOST': 'localhost',
    'PORT': '3306',
}

READONLY_LOCAL_DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'cst',
    'USER': 'root',
    'PASSWORD': 'root',
    'HOST': 'localhost',
    'PORT': '3306',
}

#*******************************************************************************#
