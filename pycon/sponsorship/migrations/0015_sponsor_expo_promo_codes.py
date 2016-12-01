# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0014_sponsor_small_entity_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='expo_promo_codes',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
    ]
