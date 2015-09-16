# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0007_auto_20150903_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialaidreviewdata',
            name='cash_check',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Payment type', choices=[(1, 'Cash'), (2, 'Check')]),
        ),
    ]
