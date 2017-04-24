# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('info', jsonfield.fields.JSONField(default={}, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='crawler',
            name='type',
            field=models.IntegerField(default=0, choices=[(0, b'Terminal'), (1, b'Browser')]),
        ),
        migrations.AddField(
            model_name='summary',
            name='crawler',
            field=models.ForeignKey(related_name='summary', to='crawlers.Crawler'),
        ),
        migrations.AlterIndexTogether(
            name='summary',
            index_together=set([('crawler', 'start_time', 'end_time')]),
        ),
    ]
