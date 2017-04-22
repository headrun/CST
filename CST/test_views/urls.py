from django.conf.urls import url

from test_views import views


urlpatterns = [
    url(r'^test/$', views.test_view),
]
