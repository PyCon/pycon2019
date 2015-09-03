# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0006_auto_20150827_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialaidapplication',
            name='experience_level',
            field=models.CharField(help_text='What is your experience level with Python?', max_length=200, verbose_name='Python experience level', choices=[(b'Beginner', 'Beginner'), (b'Intermediate', 'Intermediate'), (b'Expert', 'Expert')]),
        ),
    ]
