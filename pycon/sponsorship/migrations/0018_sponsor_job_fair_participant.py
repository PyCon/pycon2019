# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0017_sponsorship_form_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='job_fair_participant',
            field=models.BooleanField(default=False),
        ),
    ]
