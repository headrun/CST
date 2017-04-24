from django.contrib import admin

from accounts import models


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_client', 'is_active', 'created_at', )

admin.site.register(models.Profile, AccountsAdmin)
