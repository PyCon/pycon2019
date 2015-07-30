# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from decimal import Decimal
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialAidApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('pyladies_grant_requested', models.BooleanField(default=False, help_text='Would you like to be considered for a PyLadies grant? (Women only.)', verbose_name='PyLadies grant')),
                ('international', models.BooleanField(default=False, help_text='Will you be traveling internationally?', verbose_name='International')),
                ('amount_requested', models.DecimalField(default=Decimal('0.00'), help_text='Please enter the amount of assistance you need, in US dollars.', verbose_name='Amount', max_digits=8, decimal_places=2)),
                ('travel_plans', models.CharField(help_text='Please describe your travel plans', max_length=1024, verbose_name='Travel plans')),
                ('profession', models.CharField(help_text='What is it that you do', max_length=500, verbose_name='Profession')),
                ('involvement', models.CharField(help_text='Describe your involvement in any open source projects or community.', max_length=1024, verbose_name='Involvement', blank=True)),
                ('what_you_want', models.CharField(help_text='What do you want to get out of attending PyCon?', max_length=500, verbose_name='What you want')),
                ('portfolios', models.CharField(help_text='Please provide links to any portfolios you have that contain Python work. (e.g. Github, Bitbucket, etc.)', max_length=500, verbose_name='Portfolios', blank=True)),
                ('use_of_python', models.CharField(help_text='Describe your use of Python', max_length=500, verbose_name='Use of Python')),
                ('presenting', models.IntegerField(help_text='Will you be speaking, hosting a poster session, or otherwise presenting at PyCon?', verbose_name='Presenting', choices=[(1, 'Yes'), (2, 'No'), (3, "I have applied but don't know yet")])),
                ('experience_level', models.CharField(help_text='What is your experience level with Python?', max_length=200, verbose_name='Python experience level')),
                ('first_time', models.BooleanField(default=True, help_text='Is this your first time attending PyCon?', verbose_name='First time')),
                ('presented', models.BooleanField(default=False, help_text='Have you spoken at PyCon in the past?', verbose_name='Presented')),
                ('user', models.OneToOneField(related_name='financial_aid', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FinancialAidApplicationPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FinancialAidEmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('template', models.TextField(help_text="Django template used to compose text email to applicants.Context variables include 'application' and 'review'")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FinancialAidMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visible', models.BooleanField(default=False, help_text='Whether message is visible to applicant')),
                ('message', models.TextField()),
                ('submitted_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('application', models.ForeignKey(related_name='messages', to='finaid.FinancialAidApplication')),
                ('user', models.ForeignKey(help_text='User who submitted the message', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['submitted_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FinancialAidReviewData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Submitted'), (2, 'Withdrawn'), (3, 'Information needed'), (4, 'Offered'), (8, 'Requesting more funds'), (5, 'Rejected'), (6, 'Declined'), (7, 'Accepted')])),
                ('amount', models.DecimalField(default=Decimal('0.00'), max_digits=8, decimal_places=2)),
                ('grant_letter_sent', models.DateField(null=True, blank=True)),
                ('cash_check', models.IntegerField(blank=True, null=True, choices=[(1, 'Cash'), (2, 'Check')])),
                ('notes', models.TextField(blank=True)),
                ('travel_cash_check', models.IntegerField(blank=True, null=True, choices=[(1, 'Cash'), (2, 'Check')])),
                ('disbursement_notes', models.TextField(blank=True)),
                ('promo_code', models.CharField(max_length=20, blank=True)),
                ('application', models.OneToOneField(related_name='review', editable=False, to='finaid.FinancialAidApplication')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
