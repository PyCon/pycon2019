# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=20, choices=[(b'applied', b'applied'), (b'invited', b'invited'), (b'declined', b'declined'), (b'rejected', b'rejected'), (b'member', b'member'), (b'manager', b'manager')])),
                ('message', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('access', models.CharField(max_length=20, choices=[(b'open', b'open'), (b'application', b'by application'), (b'invitation', b'by invitation')])),
                ('created', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('manager_permissions', models.ManyToManyField(related_name='manager_teams', to='auth.Permission', blank=True)),
                ('permissions', models.ManyToManyField(related_name='member_teams', to='auth.Permission', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='membership',
            name='team',
            field=models.ForeignKey(related_name='memberships', to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(related_name='memberships', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('user', 'team')]),
        ),
    ]
