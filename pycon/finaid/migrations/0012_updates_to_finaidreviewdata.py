# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0011_receipt_logged'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialaidreviewdata',
            name='cash_check',
        ),
        migrations.AddField(
            model_name='financialaidreviewdata',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='financialaidreviewdata',
            name='legal_name',
            field=models.CharField(max_length=2048, blank=True),
        ),
        migrations.AddField(
            model_name='financialaidreviewdata',
            name='reimbursement_method',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Reimbursement Method', choices=[(1, 'Check'), (2, 'Wire Transfer'), (3, 'PayPal')]),
        ),
    ]
