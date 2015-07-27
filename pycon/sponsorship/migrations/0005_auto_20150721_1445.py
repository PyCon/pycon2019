# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0004_remove_sponsor_contact_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='company_description_benefit',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='print_description_benefit',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='web_logo_benefit',
        ),
        migrations.AddField(
            model_name='sponsor',
            name='booth_number',
            field=models.IntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='job_fair_table_number',
            field=models.IntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='registration_promo_codes',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='web_description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='web_logo',
            field=models.ImageField(upload_to=b'sponsor_files', null=True, verbose_name='Company logo (to show on the web site)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='display_url',
            field=models.URLField(verbose_name='display URL - text to display on link to sponsor page, if different from the actual link', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='external_url',
            field=models.URLField(verbose_name='external URL - link to sponsor web page'),
            preserve_default=True,
        ),
    ]
