# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('type', models.CharField(default=b'simple', max_length=10, verbose_name='type', choices=[(b'text', b'Text'), (b'richtext', b'Rich Text'), (b'file', b'File'), (b'weblogo', b'Web Logo'), (b'simple', b'Simple')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BenefitLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_words', models.PositiveIntegerField(null=True, verbose_name='max words', blank=True)),
                ('other_limits', models.CharField(max_length=200, verbose_name='other limits', blank=True)),
                ('benefit', models.ForeignKey(related_name='benefit_levels', verbose_name='benefit', to='sponsorship.Benefit')),
            ],
            options={
                'ordering': ['level'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Sponsor Name')),
                ('display_url', models.URLField(verbose_name='display URL', blank=True)),
                ('external_url', models.URLField(verbose_name='external URL')),
                ('annotation', models.TextField(verbose_name='annotation', blank=True)),
                ('contact_name', models.CharField(max_length=100, verbose_name='Contact Name')),
                ('contact_email', models.EmailField(max_length=75, verbose_name='Contact Email')),
                ('contact_phone', models.CharField(max_length=32, verbose_name='Contact Phone')),
                ('contact_address', models.TextField(verbose_name='Contact Address')),
                ('added', models.DateTimeField(default=datetime.datetime.now, verbose_name='added')),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('approval_time', models.DateTimeField(null=True, editable=False, blank=True)),
                ('wants_table', models.BooleanField(default=False, verbose_name='Does your organization want a table at the job fair?')),
                ('wants_booth', models.BooleanField(default=False, verbose_name='Does your organization want a booth on the expo floor?')),
                ('web_logo_benefit', models.NullBooleanField(help_text='Web logo benefit is complete')),
                ('print_logo_benefit', models.NullBooleanField(help_text='Print logo benefit is complete')),
                ('print_description_benefit', models.NullBooleanField(help_text='Print description benefit is complete')),
                ('company_description_benefit', models.NullBooleanField(help_text='Company description benefit is complete')),
                ('advertisement_benefit', models.NullBooleanField(help_text='Advertisement benefit is complete')),
                ('applicant', models.ForeignKey(related_name='sponsorships', verbose_name='applicant', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'sponsor',
                'verbose_name_plural': 'sponsors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsorBenefit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('max_words', models.PositiveIntegerField(null=True, verbose_name='max words', blank=True)),
                ('other_limits', models.CharField(max_length=200, verbose_name='other limits', blank=True)),
                ('text', models.TextField(verbose_name='text', blank=True)),
                ('upload', models.FileField(upload_to=b'sponsor_files', verbose_name='file', blank=True)),
                ('is_complete', models.NullBooleanField(help_text='True - benefit complete; False - benefit incomplete; Null - n/a')),
                ('benefit', models.ForeignKey(related_name='sponsor_benefits', verbose_name='benefit', to='sponsorship.Benefit')),
                ('sponsor', models.ForeignKey(related_name='sponsor_benefits', verbose_name='sponsor', to='sponsorship.Sponsor')),
            ],
            options={
                'ordering': ['-active'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsorLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('cost', models.PositiveIntegerField(verbose_name='cost')),
                ('description', models.TextField(help_text='This is private.', verbose_name='description', blank=True)),
                ('conference', models.ForeignKey(verbose_name='conference', to='conference.Conference')),
            ],
            options={
                'ordering': ['conference', 'order'],
                'verbose_name': 'sponsor level',
                'verbose_name_plural': 'sponsor levels',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='level',
            field=models.ForeignKey(verbose_name='level', to='sponsorship.SponsorLevel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='sponsor_logo',
            field=models.ForeignKey(related_name='+', blank=True, editable=False, to='sponsorship.SponsorBenefit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benefitlevel',
            name='level',
            field=models.ForeignKey(related_name='benefit_levels', verbose_name='level', to='sponsorship.SponsorLevel'),
            preserve_default=True,
        ),
    ]
