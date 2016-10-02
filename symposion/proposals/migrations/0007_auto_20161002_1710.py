# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0006_auto_20160928_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalbase',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
