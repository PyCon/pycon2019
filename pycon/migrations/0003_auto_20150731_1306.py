# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0002_remove_old_google_openid_auths'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pycontutorialproposal',
            name='registrants',
            field=models.ManyToManyField(help_text='CTE registered participants for this tutorial.', to=settings.AUTH_USER_MODEL, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
