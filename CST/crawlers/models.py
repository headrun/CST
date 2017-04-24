#!/usr/bin/env python

from django.contrib.auth.models import User
from django.db import models
from django.db import IntegrityError
from django.utils import timezone

from jsonfield import JSONField

from projects import models as project_models


class Crawler(models.Model):
    user = models.ForeignKey(User, related_name='crawlers')
    project = models.ForeignKey(project_models.Project, related_name='crawlers')
    name = models.CharField(max_length=255, null=False, blank=False)
    machine_ip = models.GenericIPAddressField(null=False, blank=False)
    machine_path = models.TextField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    info = JSONField(default={}, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'project', 'name', ), )
        index_together = (('user', 'project', 'name', ), )

    def __unicode__(self):
        return 'added by: {} crawler: {}, status: {}'.format(
            self.user.username, self.name, self.is_active)

    def delete(self):
        self.is_active = False
        self.deactivated_at = timezone.now()
        self.save()

    def mark_as_delete(self):
        self.delete()


# class Summary(models.Model):
#     crawler = models.ForeignKey(Crawler, related_name='summary')
#     info = JSONField(default={}, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = (('client', 'name'), )
#         index_together = (('client', 'name'), )

#     def __unicode__(self):
#         return 'crawler: {}'.format(self.crawler.name)
