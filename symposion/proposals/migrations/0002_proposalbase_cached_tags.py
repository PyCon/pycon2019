# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalbase',
            name='cached_tags',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
