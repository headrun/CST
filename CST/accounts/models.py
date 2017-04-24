
from django.contrib.auth.models import User
from django.db import models
from django.db import IntegrityError
from django.utils import timezone

from jsonfield import JSONField


class Profile(models.Model):

    user = models.OneToOneField(User, related_name='profile')
    is_client = models.BooleanField(blank=True, default=False)
    is_active = models.BooleanField(blank=True, default=True)
    extra = JSONField(default={}, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

    def delete(self):
        self.user.is_active = False
        self.save()

    def mark_as_delete(self):
        self.delete()
