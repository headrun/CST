#!/usr/bin/env python

from django.contrib.auth.models import User
from django.db import models
from django.db import IntegrityError
from django.utils import timezone

from jsonfield import JSONField


class Client(models.Model):
    admin = models.OneToOneField(User, related_name='client')
    name = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    info = JSONField(default={}, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('admin', 'name', ), )
        index_together = (('admin', 'name', ), )

    def __unicode__(self):
        return 'added by: {} client: {}, status: {}'.format(
            self.admin.username, self.name, self.is_active)

    def delete(self):
        self.is_active = False
        self.deactivated_at = timezone.now()
        self.save()

    def mark_as_delete(self):
        self.delete()


class Project(models.Model):
    client = models.ForeignKey(Client, related_name='projects')
    name = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    info = JSONField(default={}, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('client', 'name', ), )
        index_together = (('client', 'name', ), )

    def __unicode__(self):
        return 'client: {} project: {}, status: {}'.format(
            self.client.name, self.name, self.is_active)

    def delete(self):
        self.is_active = False
        self.deactivated_at = timezone.now()
        self.save()

    def mark_as_delete(self):
        self.delete()
