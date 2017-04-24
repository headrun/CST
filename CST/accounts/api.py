#!/usr/bin/python

import json

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User

from tastypie.authentication import ApiKeyAuthentication
from tastypie.authentication import MultiAuthentication
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden
from tastypie.http import HttpNotFound
from tastypie.http import HttpUnauthorized
from tastypie.resources import Resource
from tastypie.utils.urls import trailing_slash

from accounts import exceptions
from accounts import mod
from retailone import api_utils


class AccountResource(Resource):
    class Meta:
        resource_name = 'accounts'
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication(require_active=True))
        authorization = DjangoAuthorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/signup%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('signup'), name="api_signup"),
            url(r"^(?P<resource_name>%s)/register%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name="api_register"),
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    @api_utils.required(params=['username', 'password'])
    def signup(self, request, username, password, *args, **kwargs):
        self.method_check(request, allowed=['post'])
        body = json.loads(request.body)
        user = request.user
        try:
            resp = mod.signup(user, username, password, data=body)
        except exceptions.UserAlreadyLoggedInError as e:
            error = e.get_error_response()
            return self.error_response(request, error, HttpForbidden)

        return self.create_response(request, resp)

    def register(self, request, **kwargs):
        self.method_check(request, allowed=['post', 'put'])
        self.is_authenticated(request)
        user = request.user
        data = json.loads(request.body)
        result = mod.register(user, data)
        return self.create_response(request, result)

    @api_utils.required(params=['username', 'password'])
    def login(self, request, username, password, *args, **kwargs):
        self.method_check(request, allowed=['post'])
        body = json.loads(request.body)
        try:
            result = mod.login(request, username, password, data=body)
        except exceptions.InvalidUserNameOrPasswordError as e:
            error = e.get_error_response()
            return self.error_response(request, error, HttpUnauthorized)
        except exceptions.AccountDisabledError as e:
            error = e.get_error_response()
            return self.error_response(request, error, HttpForbidden)

        return self.create_response(request, result)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get', 'post'])
        logout(request)
        return self.create_response(request, {'success': True})
