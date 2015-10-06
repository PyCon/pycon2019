# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import symposion.speakers.models


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='photo',
            field=models.ImageField(upload_to=symposion.speakers.models.get_photo_path, blank=True),
        ),
    ]
