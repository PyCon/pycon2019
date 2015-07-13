# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100, db_index=True)),
                ('content', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(related_name='boxes', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(related_name='updated_boxes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'boxes',
            },
            bases=(models.Model,),
        ),
    ]
