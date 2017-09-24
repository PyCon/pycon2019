# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0005_auto_20161002_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='financial_support',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='speaker',
            name='interested_mentee',
            field=multiselectfield.db.fields.MultiSelectField(max_length=47, choices=[(b'brainstorming', b'Brainstorming'), (b'proposal_creation', b'Proposal Creation'), (b'proposal_review', b'Proposal Review')]),
        ),
        migrations.AddField(
            model_name='speaker',
            name='interested_mentor',
            field=multiselectfield.db.fields.MultiSelectField(max_length=47, choices=[(b'brainstorming', b'Brainstorming'), (b'proposal_creation', b'Proposal Creation'), (b'proposal_review', b'Proposal Review')]),
        ),
    ]
