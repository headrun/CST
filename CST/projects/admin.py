#!/usr/bin/env python

from django.contrib import admin

from projects import models


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('admin', 'name', 'is_active', 'deactivated_at', 'created_at', )


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('client', 'name', 'is_active', 'created_at', )


admin.site.register(models.Client, ClientsAdmin)
admin.site.register(models.Project, ProjectsAdmin)
