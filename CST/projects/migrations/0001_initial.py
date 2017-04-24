# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('deactivated_at', models.DateTimeField(null=True, blank=True)),
                ('info', jsonfield.fields.JSONField(default={}, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(related_name='client', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('deactivated_at', models.DateTimeField(null=True, blank=True)),
                ('info', jsonfield.fields.JSONField(default={}, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(related_name='projects', to='projects.Client')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('client', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='project',
            index_together=set([('client', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together=set([('admin', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='client',
            index_together=set([('admin', 'name')]),
        ),
    ]
