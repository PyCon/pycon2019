# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0009_auto_20150917_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialaidapplication',
            name='portfolios',
        ),
        migrations.RemoveField(
            model_name='financialaidapplication',
            name='use_of_python',
        ),
        migrations.AlterField(
            model_name='financialaidapplication',
            name='involvement',
            field=models.CharField(help_text='Describe your involvement in any open source projects or community.', max_length=1024, verbose_name='Your involvement', blank=True),
        ),
        migrations.AlterField(
            model_name='financialaidapplication',
            name='presenting',
            field=models.IntegerField(help_text='Will you be speaking, hosting a poster session, or otherwise presenting at this PyCon?', verbose_name='Presenting', choices=[(1, 'Yes'), (2, 'No'), (3, "I have applied but don't know yet")]),
        ),
        migrations.AlterField(
            model_name='financialaidapplication',
            name='profession',
            field=models.CharField(help_text='What is your career, or where are you a student?', max_length=500, verbose_name='Profession'),
        ),
        migrations.AlterField(
            model_name='financialaidapplication',
            name='travel_plans',
            field=models.CharField(help_text='Please describe your travel plans,  including the country you will travel from.', max_length=1024, verbose_name='Travel plans'),
        ),
        migrations.AlterField(
            model_name='financialaidapplication',
            name='what_you_want',
            field=models.CharField(help_text='Please tell us how you use Python currently, and what you hope to get out of attending PyCon.', max_length=500, verbose_name='How you use Python and how PyCon will help'),
        ),
    ]
