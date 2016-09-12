# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0004_auto_20150923_0743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proposalbase',
            options={'ordering': ['title']},
        ),
    ]
