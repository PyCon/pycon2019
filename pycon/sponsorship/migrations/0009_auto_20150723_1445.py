# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multi_email_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0008_remove_obsolete_benefit_records'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='contact_emails',
            field=multi_email_field.fields.MultiEmailField(default=b'', help_text='Please enter one email address per line.', verbose_name='Contact Emails'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='display_url',
            field=models.URLField(verbose_name='Link text - text to display on link to sponsor page, if different from the actual link', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='external_url',
            field=models.URLField(verbose_name='Link to sponsor web page'),
            preserve_default=True,
        ),
    ]
