# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0009_auto_20161002_1710'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SpecialEvent',
            new_name='ScheduledEvent',
        ),
        migrations.AlterModelOptions(
            name='scheduledevent',
            options={'verbose_name': 'PyCon Scheduled Event'},
        ),
    ]
