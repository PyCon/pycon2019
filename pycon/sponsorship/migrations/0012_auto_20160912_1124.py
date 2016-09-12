# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0011_auto_20150824_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='wants_booth',
            field=models.BooleanField(default=False, verbose_name='Does your organization want a booth on the expo floor? (See <a href="/2017/sponsors/fees/">Estimated Sponsor Fees</a> for costs that might be involved.)'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='wants_table',
            field=models.BooleanField(default=False, verbose_name='Does your organization want a table at the job fair? (See <a href="/2017/sponsors/fees/">Estimated Sponsor Fees</a> for costs that might be involved.)'),
        ),
    ]
