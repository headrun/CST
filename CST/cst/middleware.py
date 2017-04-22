from datetime import date, datetime, timedelta
from datetime import time as datetime_time
import dateutil
import functools
import hashlib
from HTMLParser import HTMLParser
import os
import pytz
import re
import StringIO
from sys import getsizeof
import time
import urllib2
import uuid

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.middleware import csrf
from django.template import Context
from django.template import Template
from django.utils import timezone
from django.utils.log import getLogger
from django.utils.timezone import now

from cst import cypher


logger = getLogger('django.request')


class IPCheckMiddleware(object):
    """This class will check for inmy allowed intern ip(s) or return 403"""

    def process_request(self, request):
        if request.GET.get('username') and request.GET.get('api_key'):
            # if api ky login, do not do anything
            return

        remote_addr = request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
        if not remote_addr in settings.INTERNAL_IPS:
            return HttpResponse('&#128561; !! you can\'t touch me &#128514; &#128514; &#128514;  !', status=403)


class TimezoneMiddleware(object):
    """Activates django timezone for the user based on user-profile settings."""
    def process_request(self, request):
        if not request.user.is_authenticated():
            return
        try:
            tz = request.user.profile.timezone
            if not tz:
                return
            timezone.activate(tz)
        except ValueError:
            logger.warning('Bad timezone value:(%s) for user:(%s). Falling back'
                           ' to default timezone.', tz, request.user.id)
        except Exception:
            pass


class RemoteUserMiddleware(object):
    def process_response(self, request, response):
        if not hasattr(request, 'user'):
            return response
        if request.user.is_authenticated():
            try:
                response['X-Remote-User-Name'] = request.user.username
                response['X-Remote-User-Id'] = request.user.id
            except TypeError as e:
                logger.exception('%s : %s' % (str(e), response.__class__))
        return response


class CsrfCookieMiddleware(csrf.CsrfViewMiddleware):
    """ Middleware to ensure that the csrf cookie is set for all GET requests.

    Subclasses django's CsrfViewMiddleware.
    """
    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        Ensures that the csrf cookie is set for all GET requests, by
        calling django.middleware.csrf.get_token, which sets
        request.META["CSRF_COOKIE_USED"] to True.

        This is exactly what django's 'ensure_csrf_cookie' decorator does
        https://github.com/django/django/blob/1.5.1/django/views/decorators/csrf.py#L32
        """

        retval = super(CsrfCookieMiddleware, self).process_view(
                request, callback, callback_args, callback_kwargs)

        # Force process_response to set the cookie on all GET requests
        if request.method == "GET":
            csrf.get_token(request)

        return retval
