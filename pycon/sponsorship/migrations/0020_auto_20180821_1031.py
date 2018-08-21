# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0019_auto_20180723_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='print_logo',
            field=models.FileField(upload_to=b'sponsor_files', null=True, verbose_name='Print logo (For printed materials, signage, and projection. SVG or EPS)'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='packages',
            field=models.ManyToManyField(to='sponsorship.SponsorPackage', verbose_name='packages', blank=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='web_logo',
            field=models.ImageField(upload_to=b'sponsor_files', null=True, verbose_name='Web logo (For display on our sponsors page. High resolution PNG or JPG)'),
        ),
    ]
