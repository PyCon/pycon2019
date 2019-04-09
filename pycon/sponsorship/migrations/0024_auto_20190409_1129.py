# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0023_auto_20181106_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='booth_number',
            field=models.CharField(default=None, max_length=5, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='job_fair_table_number',
            field=models.CharField(default=None, max_length=5, null=True, blank=True),
        ),
    ]
