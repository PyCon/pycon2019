# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0005_auto_20150827_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialaidreviewdata',
            name='travel_cash_check',
        ),
        migrations.RemoveField(
            model_name='financialaidreviewdata',
            name='when_grant_letter_sent',
        ),
        migrations.AlterField(
            model_name='financialaidreviewdata',
            name='cash_check',
            field=models.IntegerField(blank=True, help_text=b'Payment type', null=True, choices=[(1, 'Cash'), (2, 'Check')]),
        ),
    ]
