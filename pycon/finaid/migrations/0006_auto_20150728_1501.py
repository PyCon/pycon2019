# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0005_receipt_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='description',
            field=models.CharField(help_text=b'Please enter a description of this receipt image.', max_length=255),
            preserve_default=True,
        ),
    ]
