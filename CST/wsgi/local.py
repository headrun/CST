#!/usr/bin/env python
"""
WSGI config for CST project.

"""

from os import getenv 
from os.path import abspath, dirname, join

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
