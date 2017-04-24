"""URL Routes for payment
"""
from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'accounts.views',
    url(r'^login/$', 'login'),
)
