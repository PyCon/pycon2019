# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='As you would like it to appear in the conference program.', max_length=100)),
                ('biography', models.TextField(help_text='A little bit about you. 100 words or less, please. This will be used in print publications so please keep it simple, no links or formatting.')),
                ('photo', models.ImageField(upload_to=b'speaker_photos', blank=True)),
                ('twitter_username', models.CharField(help_text='Your Twitter account', max_length=15, blank=True)),
                ('annotation', models.TextField()),
                ('invite_email', models.CharField(max_length=200, unique=True, null=True, db_index=True)),
                ('invite_token', models.CharField(max_length=40, db_index=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('sessions_preference', models.IntegerField(blank=True, help_text="If you've submitted multiple talk proposals, please let us know if you only want to give one or if you'd like to give two talks.  For tutorials and posters, state similar preferences in the additional notes section of your proposals.", null=True, choices=[(1, 'One'), (2, 'Two')])),
                ('user', models.OneToOneField(related_name='speaker_profile', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
    ]
