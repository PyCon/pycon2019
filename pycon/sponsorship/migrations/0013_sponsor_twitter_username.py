# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0012_auto_20160912_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='twitter_username',
            field=models.CharField(max_length=15, verbose_name='Twitter username', blank=True),
        ),
    ]
