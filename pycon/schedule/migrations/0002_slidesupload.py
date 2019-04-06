# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pycon.schedule.models


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_schedule', '0002_auto_20150723_0856'),
        ('pycon_schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlidesUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slides', models.FileField(upload_to=pycon.schedule.models.get_presentation_upload_path, verbose_name=b'PDF export of your slides')),
                ('presentation', models.ForeignKey(to='symposion_schedule.Presentation')),
            ],
        ),
    ]
