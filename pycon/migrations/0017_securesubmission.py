# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pycon', '0016_auto_20190215_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecureSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('submission_type', models.IntegerField(verbose_name=b'Submission Type', choices=[(1, 'Financial Aid Recipient - Reimbursement Method Details (Bank, ACH, PayPal, or similar)'), (2, 'Tutorial Presenter - Payment Details (Bank, ACH, PayPal, or similar)'), (3, 'Tutorial Presenter - Tax Form (W-9, W-8, or similar form)')])),
                ('description', models.CharField(default=b'No description provided', max_length=1024)),
                ('message', django_cryptography.fields.encrypt(models.TextField(default=None, null=True, blank=True))),
                ('file_attachment', django_cryptography.fields.encrypt(models.BinaryField(default=None, null=True, blank=True))),
                ('file_attachment_name', models.CharField(default=None, max_length=2048, null=True, blank=True)),
                ('file_attachment_content_type', models.CharField(default=None, max_length=2048, null=True, blank=True)),
                ('logged', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='secure_submissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_view_secure_submissions', 'View Secure Submissions'),),
            },
        ),
    ]
