# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0022_auto_20180828_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='a_la_carte_registration_promo_codes',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='additional_discounted_registration_promo_codes',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
    ]
