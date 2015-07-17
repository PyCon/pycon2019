# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pycon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PyConTutorialMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('submitted_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('tutorial', models.ForeignKey(related_name='tutorial_messages', to='pycon.PyConTutorialProposal')),
                ('user', models.ForeignKey(help_text='User who submitted the message', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-submitted_at'],
            },
            bases=(models.Model,),
        ),
    ]
