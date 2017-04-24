# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crawler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('machine_ip', models.GenericIPAddressField()),
                ('machine_path', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('deactivated_at', models.DateTimeField(null=True, blank=True)),
                ('info', jsonfield.fields.JSONField(default={}, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(related_name='crawlers', to='projects.Project')),
                ('user', models.ForeignKey(related_name='crawlers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='crawler',
            unique_together=set([('user', 'project', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='crawler',
            index_together=set([('user', 'project', 'name')]),
        ),
    ]
