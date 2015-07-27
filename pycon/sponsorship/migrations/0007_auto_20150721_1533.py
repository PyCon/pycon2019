# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0006_migrate_web_description_and_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='sponsor_logo',
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='applicant',
            field=models.ForeignKey(related_name='sponsorships', on_delete=django.db.models.deletion.SET_NULL, verbose_name='applicant', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='web_description',
            field=models.TextField(verbose_name='Company description (to show on the web site)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='web_logo',
            field=models.ImageField(upload_to=b'sponsor_files', null=True, verbose_name='Company logo (to show on the web site)'),
            preserve_default=True,
        ),
    ]
