# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0021_auto_20180821_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorlevel',
            name='display',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sponsorpackage',
            name='display',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='web_logo',
            field=models.ImageField(help_text='For display on our sponsor webpage. High resolution PNG or JPG, smallest dimension no less than 256px', upload_to=b'sponsor_files', null=True, verbose_name='Web logo'),
        ),
    ]
