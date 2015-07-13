# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import symposion.cms.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=symposion.cms.models.generate_filename)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('path', models.CharField(unique=True, max_length=100)),
                ('body', models.TextField()),
                ('body_fr', models.TextField(blank=True)),
                ('status', models.IntegerField(default=2, choices=[(1, 'Draft'), (2, 'Public')])),
                ('publish_date', models.DateTimeField(default=datetime.datetime.now)),
                ('created', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('updated', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
