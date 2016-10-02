# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0008_auto_20161002_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pycontutorialproposal',
            name='outline',
            field=models.TextField(),
        ),
    ]
