from functools import wraps

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.http import Http404
from django_mobile import get_flavour
from django_mobile.conf import settings as mobile_settings


def cache_tag(ttl=1200):
    """
    Decorator that caches the result of a method for the specified time in seconds.

    Use it as:

      @cached(ttl=1200)
      def functionToCache(arguments):
        ...
    """
    def decorator(function):
        @wraps(function)
        def wrapper(context, *args, **kwargs):
            args_key = ':'.join([str(x) for x in args])
            kwargs_key = ':'.join(['%s|%s' % (str(k), str(kwargs[k])) for k in kwargs])
            key = '%s/%s/%s' % (function.__name__, args_key, kwargs_key) 
            value = cache.get(key, version=settings.CACHE_VERSION)
            if not value:
                value = function(context, *args, **kwargs)
                cache.set(
                    key, value, timeout=ttl,
                    version=settings.CACHE_VERSION)
            return value
        return wrapper
    return decorator


class cached(object):

    def __init__(self, key, ttl):
        self.key = key
        self.ttl = ttl

    def __call__(self, func):
        def inner(*args, **kwargs):
            key = '%s/%s' % (self.key, ':'.join([str(x) for x in args]))
            result = cache.get(key, version=settings.CACHE_VERSION)
            if result:
                return result
            result = func(*args, **kwargs)
            cache.set(
                key, result, timeout=self.ttl,
                version=settings.CACHE_VERSION)
            return result
        return inner


def staff_member_or_404(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, else throws 404 error.
    """
    @wraps(view_func)
    def _checkstaff(request, *args, **kwargs):
        user = request.user
        if user.is_active and (user.is_superuser or user.is_staff):
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)
        raise Http404()
    return _checkstaff


def group_member_or_404(group_name):
    """Decorator for views that checks that the user is logged in and
    is member of the the group."""
    def _check_member(view_func):
        @wraps(view_func)
        def _validator(request, *args, **kwargs):
            user = request.user
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                raise Http404()
            if user in group.user_set.all():
                return view_func(request, *args, **kwargs)
            raise Http404()
        return _validator
    return _check_member


def groups_member_or_404(group_names):
    """Decorator for views that checks that the user is logged in and
    is member of any of the group."""
    def _check_member(view_func):
        @wraps(view_func)
        def _validator(request, *args, **kwargs):
            if not isinstance(group_names, list):
                raise Http404()
            user = request.user
            user_group_names = set(user.groups.values_list('name', flat=True))
            if set(group_names) & user_group_names:
                return view_func(request, *args, **kwargs)
            raise Http404()
        return _validator
    return _check_member
