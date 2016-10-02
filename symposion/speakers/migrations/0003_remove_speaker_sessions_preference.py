# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0002_auto_20151006_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speaker',
            name='sessions_preference',
        ),
    ]
