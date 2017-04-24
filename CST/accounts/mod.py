import hashlib
import random
import string
import time

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User, UserManager
from django.db import IntegrityError
from django.utils import timezone

from tastypie.models import ApiKey

from accounts import constants
from accounts import exceptions
from accounts import models
from accounts import utils


# Public
######################

def login(request, username, password, data={}):
    if username and '@' in username:
        username = utils.get_username_from_email(username)
    user = authenticate(username=username, password=password)
    if not user:
        raise exceptions.InvalidUserNameOrPasswordError

    if not user.is_active:
        raise exceptions.AccountDisabledError
    
    django_login(request, user)
    result = {'success': True}
    
    require_api_key = data.get('require_api_key', False)
    if require_api_key:
        result['apikey'] = _get_api_key(user)

    require_profile = data.get('require_profile', False)
    if require_profile:
        result['profile'] = user.profile.get_dict()
    return result


def register(user, data):
    if data.get('first_name') or data.get('last_name'):
        user.first_name = data.get('first_name') or user.first_name
        user.last_name = data.get('last_name') or user.last_name
        user.save()

    profile = user.profile
    if 'dob' in req and req['dob'] != '':
        profile.dob = utils.convert_date(req['dob'])

    profile.timezone = data.get('timezone', '')
    profile.set_registration_done()
    profile.save()
    return {'success': True, 'profile': profile.get_dict()}


def signup(user, username, password, data):
    name = data.get('name').strip()
    email = data.get('email').strip()
    require_api_key = data.get('require_api_key', False)
    valid_user, response = _can_user_signup(username)
    if not valid_user:
        return response
    result = {'success': True}

    if user.is_authenticated():
        profile = user.profile
        if profile.is_temporary_user:
            user = _update_temporary_user(user, username, password, name)
            profile.set_temp_user(False)
        raise exceptions.UserAlreadyLoggedInError
    _create_user(username, email=email, password=password, name=name)
    if require_api_key:
        result['apikey'] = _get_api_key(user)
    return result


# Private
######################

def _get_api_key(user):
    try:
        return ApiKey.objects.get(user=user).key
    except ApiKey.DoesNotExist:
        api_key = ApiKey.objects.create(user=user)
        return api_key.key


def _create_user(username, email=None, password=None, name=None, is_temp_user=False):
    first_name, last_name = _get_first_name_and_last_name(name)
    if not email:
        email = username
    try:
        if not password:
            user = User.objects.create_user(
                username=username, email=email, first_name=first_name,
                last_name=last_name)
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name)
    except IntegrityError:
        raise exceptions.UserNameAlreadyExist

    models.Profile.objects.create(
        user=user, registration_done=False, is_temp_user=is_temp_user)
    return user


def _can_user_signup(username):
    if len(username) < 1:
        return False, exceptions.InvalidUserNameOrPasswordError
    username_present, email_present = _is_username_email_present(username)
    if username_present:
        return False, exceptions.UsernameAlreadyExistError
    if email_present:
        return False, exceptions.EmailAlreadyExistError
    return True, None


def _get_first_name_and_last_name(name):
    first_name = ''
    last_name = ''
    if name:
        name = name.split(' ', 1)
        first_name = name[0]
        if len(name) > 1:
            last_name = name[1]
    return first_name, last_name


def _is_username_email_present(username):
    if not username:
        return False, False
    username_present = User.objects.filter(username=username).count() != 0
    email_present = User.objects.filter(email=username).count() != 0
    return username_present, email_present


def _update_temporary_user(user, username, password, name=None):
    email = UserManager.normalize_email(username)
    user.username = username
    user.email = email
    user.set_password(password)
    user.first_name, user.last_name = _get_first_name_and_last_name(name)
    user.save()
    return user