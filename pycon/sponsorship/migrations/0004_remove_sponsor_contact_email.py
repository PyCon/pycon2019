# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0003_migrate_sponsor_emails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='contact_email',
        ),
    ]
