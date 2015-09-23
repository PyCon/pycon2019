# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0003_set_cached_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalkind',
            name='slug',
            field=models.SlugField(help_text=b"kind slugs are lowercase and singular, e.g. 'tutorial'", unique=True),
        ),
    ]
