# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0008_auto_20161002_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalbase',
            name='abstract',
            field=models.TextField(help_text='Detailed description. Will be made public if your talk is accepted.', verbose_name='Detailed Abstract', blank=True),
        ),
    ]
