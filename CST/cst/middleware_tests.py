import datetime
import sys
from random import randint
from StringIO import StringIO

import django.http
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.utils import timezone
from django.utils.importlib import import_module

import mock
import pytz

from accounts import factoryboy
from cst.middleware import TimezoneMiddleware


class TimezoneMiddlewareTestCase(TestCase):

    def setUp(self):
        self.middleware = TimezoneMiddleware()

    @mock.patch('django.utils.timezone.activate')
    def test_tz_not_set_when_user_is_not_authenticated(self, activate):
        request = self._fake_request()
        self.middleware.process_request(request)
        self.assertFalse(activate.called, 'TZ got activated wrongly.')

    @mock.patch('django.utils.timezone.activate')
    def test_tz_not_when_user_profile_has_no_timezone_set(self, activate):
        user = factoryboy.UserFactory()
        factoryboy.UserProfileFactory(user=user, timezone='')
        request = self._fake_request(user)
        self.middleware.process_request(request)
        self.assertFalse(activate.called, 'TZ got activated wrongly.')

    @mock.patch('django.utils.timezone.activate')
    def test_tz_as_per_profile_config(self, activate):
        user = self._get_user('Asia/Hong_Kong')
        request = self._fake_request(user)
        self.middleware.process_request(request)
        activate.assert_called_with('Asia/Hong_Kong')

        user = self._get_user('Asia/Kolkata')
        request = self._fake_request(user)
        self.middleware.process_request(request)
        activate.assert_called_with('Asia/Kolkata')

    def _get_user(self, tz):
        user = factoryboy.UserFactory()
        factoryboy.UserProfileFactory(user=user, timezone=tz)
        return user

    def _fake_request(self, user=None, query_string=''):
        req = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/',
            'QUERY_STRING': query_string,
            'wsgi.input': StringIO()})
        if not user:
            user = AnonymousUser()
        req.user = user
        return req
