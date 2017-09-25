# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0009_auto_20170209_2326'),
    ]

    operations = [
        migrations.RenameField('proposalbase', 'submitted', 'submitted_at'),
        migrations.AlterField(
            model_name='proposalbase',
            name='submitted_at',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='proposalbase',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
    ]
