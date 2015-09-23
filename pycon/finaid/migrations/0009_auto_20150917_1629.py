# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pycon.finaid.models


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0008_auto_20150916_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='receipt_image',
            field=models.FileField(upload_to=pycon.finaid.models.user_directory_path),
        ),
    ]
