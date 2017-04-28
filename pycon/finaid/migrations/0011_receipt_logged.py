# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0010_auto_20160927_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='logged',
            field=models.BooleanField(default=False),
        ),
    ]
