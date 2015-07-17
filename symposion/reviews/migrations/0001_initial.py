# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from decimal import Decimal
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('public', models.BooleanField(default=False, choices=[(True, b'public'), (False, b'private')])),
                ('commented_at', models.DateTimeField(default=datetime.datetime.now)),
                ('commenter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('proposal', models.ForeignKey(related_name='comments', to='proposals.ProposalBase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LatestVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.CharField(max_length=2, choices=[(b'+1', '+1 \u2014 Good proposal and I will argue for it to be accepted.'), (b'+0', '+0 \u2014 OK proposal, but I will not argue for it to be accepted.'), ('\u22120', '\u22120 \u2014 Weak proposal, but I will not argue strongly against acceptance.'), ('\u22121', '\u22121 \u2014 Serious issues and I will argue to reject this proposal.')])),
                ('submitted_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('proposal', models.ForeignKey(related_name='votes', to='proposals.ProposalBase')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100)),
                ('from_address', models.EmailField(max_length=75)),
                ('subject', models.CharField(max_length=100)),
                ('body', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('review_start', models.DateTimeField()),
                ('vote_start', models.DateTimeField()),
                ('vote_end', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('submitted_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('proposal', models.ForeignKey(related_name='messages', to='proposals.ProposalBase')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['submitted_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(default=Decimal('0.00'), max_digits=5, decimal_places=2)),
                ('comment_count', models.PositiveIntegerField(default=0)),
                ('vote_count', models.PositiveIntegerField(default=0)),
                ('plus_one', models.PositiveIntegerField(default=0)),
                ('plus_zero', models.PositiveIntegerField(default=0)),
                ('minus_zero', models.PositiveIntegerField(default=0)),
                ('minus_one', models.PositiveIntegerField(default=0)),
                ('accepted', models.NullBooleanField(default=None, choices=[(True, b'accepted'), (False, b'rejected'), (None, b'undecided')])),
                ('status', models.CharField(default=b'undecided', max_length=20, db_index=True, choices=[(b'accepted', b'accepted'), (b'rejected', b'rejected'), (b'undecided', b'undecided'), (b'standby', b'standby')])),
                ('group', models.ForeignKey(related_name='proposal_results', blank=True, to='reviews.ProposalGroup', null=True)),
                ('proposal', models.OneToOneField(related_name='result', to='proposals.ProposalBase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResultNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('to_address', models.EmailField(max_length=75)),
                ('from_address', models.EmailField(max_length=75)),
                ('subject', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('proposal', models.ForeignKey(related_name='notifications', to='proposals.ProposalBase')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='reviews.NotificationTemplate', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.CharField(blank=True, max_length=2, choices=[(b'+1', '+1 \u2014 Good proposal and I will argue for it to be accepted.'), (b'+0', '+0 \u2014 OK proposal, but I will not argue for it to be accepted.'), ('\u22120', '\u22120 \u2014 Weak proposal, but I will not argue strongly against acceptance.'), ('\u22121', '\u22121 \u2014 Serious issues and I will argue to reject this proposal.')])),
                ('comment', models.TextField()),
                ('submitted_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('proposal', models.ForeignKey(related_name='reviews', to='proposals.ProposalBase')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin', models.IntegerField(choices=[(0, b'auto-assigned, initial'), (1, b'opted-in'), (2, b'auto-assigned, later')])),
                ('assigned_at', models.DateTimeField(default=datetime.datetime.now)),
                ('opted_out', models.BooleanField(default=False)),
                ('proposal', models.ForeignKey(to='proposals.ProposalBase')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='latestvote',
            unique_together=set([('proposal', 'user')]),
        ),
    ]
