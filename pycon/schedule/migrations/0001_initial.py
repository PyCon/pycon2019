# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('symposion_schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.ForeignKey(related_name='sessions', to='symposion_schedule.Day')),
                ('slots', models.ManyToManyField(related_name='sessions', to='symposion_schedule.Slot')),
            ],
        ),
        migrations.CreateModel(
            name='SessionRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.IntegerField(choices=[(1, b'Session Chair'), (2, b'Session Runner')])),
                ('status', models.NullBooleanField()),
                ('submitted', models.DateTimeField(default=datetime.datetime.now)),
                ('session', models.ForeignKey(to='pycon_schedule.Session')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sessionrole',
            unique_together=set([('session', 'user', 'role')]),
        ),
    ]
