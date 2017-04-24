#!/usr/bin/env python

from django.contrib import admin

from crawlers import models


class CrawlersAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'name', 'is_active', 'deactivated_at', 'created_at', )


admin.site.register(models.Crawler, CrawlersAdmin)
