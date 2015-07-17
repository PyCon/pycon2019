# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pycon.pycon_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Description of person or service using the API key.', max_length=100)),
                ('auth_key', models.CharField(default=pycon.pycon_api.models.random_uuid4, unique=True, max_length=36)),
                ('secret', models.CharField(default=pycon.pycon_api.models.random_uuid4, max_length=36)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IRCLogLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('user', models.CharField(max_length=40)),
                ('line', models.TextField(blank=True)),
                ('proposal', models.ForeignKey(to='proposals.ProposalBase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField()),
                ('proposal', models.OneToOneField(related_name='data', to='proposals.ProposalBase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
