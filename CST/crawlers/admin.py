#!/usr/bin/env python

from django.contrib import admin

from common_exceptions import common
from crawlers import models


class CrawlersAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.user == request.user or request.user.is_superuser:
            obj.save()
            return
        raise common.UnAuthorizedUserError

    def get_queryset(self, request):
        qs = super(CrawlersAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if not obj:
            return True
        return obj.user == request.user

    list_display = ('user', 'project', 'name', 'type', 'is_active', 'deactivated_at', 'created_at', )
    list_filter = (('user', admin.RelatedOnlyFieldListFilter), )


admin.site.register(models.Crawler, CrawlersAdmin)
