# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='assets_url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='presentation',
            name='slides_url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='presentation',
            name='video_url',
            field=models.URLField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
