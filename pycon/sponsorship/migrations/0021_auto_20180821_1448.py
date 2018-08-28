# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0020_auto_20180821_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='display_url',
            field=models.CharField(default=b'', max_length=200, verbose_name='Link text - text to display on link to sponsor webpage, if different from the actual link', blank=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='external_url',
            field=models.URLField(help_text='(Must include https:// or http://.)', verbose_name='Link to sponsor webpage'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='print_logo',
            field=models.FileField(help_text='For printed materials, signage, and projection. SVG or EPS', upload_to=b'sponsor_files', null=True, verbose_name='Print logo', blank=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='wants_booth',
            field=models.BooleanField(default=False, verbose_name='Does your organization want a booth on the expo floor? (See <a href="/2019/sponsors/fees/">Estimated Sponsor Fees</a> for costs that might be involved.)'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='wants_table',
            field=models.BooleanField(default=False, verbose_name='Does your organization want a table at the job fair? (See <a href="/2019/sponsors/fees/">Estimated Sponsor Fees</a> for costs that might be involved.)'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='web_logo',
            field=models.ImageField(help_text='For display on our sponsor webpage. High resolution PNG or JPG, smallest dimension no less than 250px', upload_to=b'sponsor_files', null=True, verbose_name='Web logo'),
        ),
    ]
