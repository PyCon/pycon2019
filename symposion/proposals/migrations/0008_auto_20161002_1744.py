# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0007_auto_20161002_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalbase',
            name='description',
            field=models.TextField(help_text='Both your title and this description are made public and displayed in the conference program to help attendees decide whether they are interested in this presentation. Limit this description to a few concise paragraphs.', verbose_name='Description'),
        ),
    ]
