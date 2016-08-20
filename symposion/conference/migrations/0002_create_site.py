# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_site(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Site = apps.get_model('sites', 'Site')
    db_alias = schema_editor.connection.alias
    Site.objects.using(db_alias).get_or_create(
        pk=1,
        defaults= {
            "pk": 1,
            "domain": "us.pycon.org",
            "name": "PyCon 2017"
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_site),
    ]
