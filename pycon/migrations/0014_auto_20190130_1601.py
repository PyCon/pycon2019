# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0013_pyconstartuprowapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='pyconstartuprowapplication',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pyconstartuprowapplication',
            name='company_logo',
            field=models.ImageField(help_text='For display on our website. High resolution PNG or JPG, smallest dimension no less than 256px', upload_to=b'startuprow_logos', null=True, verbose_name='Company logo'),
        ),
        migrations.AlterField(
            model_name='pyconstartuprowapplication',
            name='applicant',
            field=models.OneToOneField(related_name='startuprow_application', null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='applicant', to=settings.AUTH_USER_MODEL),
        ),
    ]
