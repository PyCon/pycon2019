# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multi_email_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='contact_emails',
            field=multi_email_field.fields.MultiEmailField(default=b'', verbose_name='Contact Emails'),
            preserve_default=True,
        ),
    ]
