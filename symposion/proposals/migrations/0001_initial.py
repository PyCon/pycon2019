# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import taggit.managers
import symposion.proposals.models


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0001_initial'),
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalSpeaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Declined')])),
            ],
            options={
                'db_table': 'proposals_proposalbase_additional_speakers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(help_text=b'If your talk is accepted this will be made public and printed in the program. Should be one paragraph, maximum 400 characters.', max_length=400, verbose_name='Description')),
                ('abstract', models.TextField(help_text='Detailed description. Will be made public if your talk is accepted.', verbose_name='Detailed Abstract')),
                ('additional_notes', models.TextField(help_text="Anything else you'd like the program committee to know when making their selection: your past speaking experience, open source community experience, etc.", blank=True)),
                ('submitted', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('cancelled', models.BooleanField(default=False)),
                ('additional_speakers', models.ManyToManyField(to='speakers.Speaker', through='proposals.AdditionalSpeaker', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalKind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', models.SlugField()),
                ('section', models.ForeignKey(related_name='proposal_kinds', to='conference.Section')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(help_text='When submissions open', null=True, blank=True)),
                ('end', models.DateTimeField(help_text='When submissions close', null=True, blank=True)),
                ('closed', models.NullBooleanField()),
                ('published', models.NullBooleanField()),
                ('section', models.OneToOneField(to='conference.Section')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupportingDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('file', models.FileField(upload_to=symposion.proposals.models.uuid_filename)),
                ('description', models.CharField(max_length=140)),
                ('proposal', models.ForeignKey(related_name='supporting_documents', to='proposals.ProposalBase')),
                ('uploaded_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='proposalbase',
            name='kind',
            field=models.ForeignKey(to='proposals.ProposalKind'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposalbase',
            name='speaker',
            field=models.ForeignKey(related_name='proposals', to='speakers.Speaker'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposalbase',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='additionalspeaker',
            name='proposalbase',
            field=models.ForeignKey(to='proposals.ProposalBase'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='additionalspeaker',
            name='speaker',
            field=models.ForeignKey(to='speakers.Speaker'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='additionalspeaker',
            unique_together=set([('speaker', 'proposalbase')]),
        ),
    ]
