#!/usr/bin/python

from django.contrib.auth.models import User
from django.http import Http404


def get_ipaddress_from_request(request):
    if not request:
        return None
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


def get_username_from_email(email):
    users = User.objects.filter(email__iexact=email).values('username')
    if not users:
        return email
    if len(users) > 1:
        raise Http404()
    return str(users[0]['username'])
