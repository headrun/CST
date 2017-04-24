"""Tests for Accounts API """

import datetime
import mock
import pytz
import json

from django.conf import settings
from django.core import mail
from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from django.test.utils import override_settings
from django.utils import timezone

from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpResponse
from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase
from test.test_support import import_module

from accounts import factoryboy
from accounts import exceptions


class AccountsApiTest(ResourceTestCase):

    def setUp(self):
        super(AccountsApiTest, self).setUp()
        self.user = factoryboy.UserFactory()
        factoryboy.UserProfileFactory(user=self.user)

        # Adding session information to the client
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.api_client.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    @mock.patch('accounts.mod.login')
    def test_login(self, login):
        login.return_value = {'success': True}
        url = '/api/v1/accounts/login'
        data = {'password': 'done', 'username': 'neelanshu'}
        resp = self.api_client.post(url, data=data)
        self.assertHttpOK(resp)
        resp = self.deserialize(resp)
        self.assertEquals(resp, {'success': True})

    @mock.patch('accounts.mod.signup')
    def test_signup(self, signup):
        data = {'password': 'done'}
        resp = self.api_client.post('/api/v1/accounts/signup', data=data)
        self.assertHttpBadRequest(resp)
        json_resp = self.deserialize(resp)
        self.assertEqual(json_resp, {
            'fields': ['username'],
            'reason': 'requiredFieldsNotPresent',
            'success': False
        })
        self.assertEquals(signup.call_count, 0)

        signup.return_value = {'success': True}
        data = {'password': 'done', 'username': 'neelanshu'}
        resp = self.api_client.post('/api/v1/accounts/signup', data=data)
        self.assertHttpOK(resp)
        resp = self.deserialize(resp)
        self.assertEquals(resp, {'success': True})
        self.assertEquals(signup.call_count, 1)

    @mock.patch('accounts.mod.signup')
    def test_signup_exceptions(self, signup):
        data = {'password': 'done', 'username': 'neelanshu'}
        signup.side_effect = exceptions.UserAlreadyLoggedInError
        resp = self.api_client.post('/api/v1/accounts/signup', data=data)
        self.assertHttpForbidden(resp)
        resp = self.deserialize(resp)
        self.assertEquals(signup.call_count, 1)
        self.assertEquals(resp, {
            'errorCode': 'userAlreadyLoggedIn',
            'errorMessage': 'The user is already logged in'})

    # @mock.patch('accounts.mod.register')
    # def test_register(self, register):
    #     data = {
    #         'dob': '1995-03-13',
    #     }
    #     resp = self.api_client.post('/api/v1/account/register/', data=data,
    #             authentication=self._get_credentials())
    #     self.assertHttpOK(resp)
    #     self.assertValidJSONResponse(resp)
    #     json_resp = self.deserialize(resp)
    #     self.assertTrue('success' in json_resp)
    #     self.assertTrue(json_resp['success'])
    #     self.assertTrue('profile' in json_resp)
    #     self.assertEquals(json_resp['profile']['dob'], '1995-03-13')

    # def _get_credentials(self, user=None):
    #     if not user:
    #         user = self.user
    #     ak = ApiKey.objects.get(user=user).key
    #     return self.create_apikey(username=user.username, api_key=ak)
