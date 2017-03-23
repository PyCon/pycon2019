# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0015_sponsor_expo_promo_codes'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorlevel',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
