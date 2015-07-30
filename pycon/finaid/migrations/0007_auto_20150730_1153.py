# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0006_auto_20150728_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='item',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='user',
        ),
    ]
