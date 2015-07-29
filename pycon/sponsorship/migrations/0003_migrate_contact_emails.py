# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forward(apps, schema_editor):
    Sponsor = apps.get_model('sponsorship', 'Sponsor')
    db_alias = schema_editor.connection.alias

    for sponsor in Sponsor.objects.using(db_alias).exclude(contact_email=''):
        sponsor.contact_emails = [sponsor.contact_email]
        sponsor.save()

def back(apps, schema_editor):
    Sponsor = apps.get_model('sponsorship', 'Sponsor')
    db_alias = schema_editor.connection.alias

    # do stuff
    for sponsor in Sponsor.objects.using(db_alias).exclude(contact_emails=''):
        sponsor.contact_email = sponsor.contact_emails[0]
        sponsor.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0002_sponsor_contact_emails'),
    ]

    operations = [
        migrations.RunPython(forward, back),
    ]
