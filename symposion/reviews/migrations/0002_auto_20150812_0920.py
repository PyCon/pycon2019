# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationtemplate',
            name='from_address',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='resultnotification',
            name='from_address',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='resultnotification',
            name='to_address',
            field=models.EmailField(max_length=254),
        ),
    ]
