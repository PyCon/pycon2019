# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0003_auto_20150827_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialaidreviewdata',
            name='grant_letter_sent',
            field=models.BooleanField(default=False),
        ),
    ]
