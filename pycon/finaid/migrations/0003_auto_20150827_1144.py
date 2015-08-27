# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0002_receipt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='financialaidreviewdata',
            old_name='grant_letter_sent',
            new_name='when_grant_letter_sent',
        ),
    ]
