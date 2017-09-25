# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0010_explicit_submit'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalbase',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='proposalbase',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
