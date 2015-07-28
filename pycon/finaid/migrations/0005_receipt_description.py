# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0004_auto_20150728_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='description',
            field=models.CharField(help_text=b'Please enter a description of this receipt image.', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
