# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pycon.finaid.models


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0002_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='new_file',
            field=models.ImageField(upload_to=pycon.finaid.models.user_directory_path),
            preserve_default=True,
        ),
    ]
