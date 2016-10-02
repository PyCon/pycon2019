# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0004_speaker_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='mobile_number',
            field=models.CharField(max_length=40, blank=True),
        ),
    ]
