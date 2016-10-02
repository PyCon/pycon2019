# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0013_sponsor_twitter_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='small_entity_discount',
            field=models.BooleanField(default=False, verbose_name='Does your organization have fewer than 25 employees, which qualifies you for our Small Entity Discount?'),
        ),
    ]
