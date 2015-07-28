# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0003_auto_20150723_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='new_file',
            new_name='receipt_image',
        ),
    ]
