# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0003_remove_speaker_sessions_preference'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='mobile_number',
            field=models.CharField(help_text='Your mobile number, that we can use to contact you at PyCon if your talk has been accepted and put on the schedule but we cannot find you when it is time.', max_length=40, blank=True),
        ),
    ]
