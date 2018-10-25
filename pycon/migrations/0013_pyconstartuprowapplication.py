# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pycon', '0012_pyconcharlaproposal'),
    ]

    operations = [
        migrations.CreateModel(
            name='PyConStartupRowApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applicant_name', models.CharField(max_length=100)),
                ('applicant_company_role', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('company_url', models.CharField(default=b'', max_length=100, blank=True)),
                ('company_location', models.CharField(max_length=100)),
                ('company_activity', models.TextField(max_length=500)),
                ('company_python_usage', models.TextField(max_length=500)),
                ('company_age', models.CharField(max_length=50)),
                ('company_size', models.CharField(max_length=50)),
                ('company_competitive_advantage', models.TextField(max_length=500)),
                ('company_monetization_strategy', models.TextField(max_length=500)),
                ('company_funding', models.CharField(default=b'', max_length=100, blank=True)),
                ('company_additional_notes', models.TextField(default=b'', max_length=500, blank=True)),
                ('company_demo_url', models.CharField(default=b'', max_length=100, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('applicant', models.ForeignKey(related_name='startuprow_applications', on_delete=django.db.models.deletion.SET_NULL, verbose_name='applicant', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'PyCon Startup Row Application',
            },
        ),
    ]
