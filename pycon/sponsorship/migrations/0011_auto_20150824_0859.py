# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0010_remove_more_benefits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='display_url',
            field=models.CharField(default=b'', max_length=200, verbose_name='Link text - text to display on link to sponsor page, if different from the actual link', blank=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='external_url',
            field=models.URLField(help_text='(Must include https:// or http://.)', verbose_name='Link to sponsor web page'),
        ),
    ]
