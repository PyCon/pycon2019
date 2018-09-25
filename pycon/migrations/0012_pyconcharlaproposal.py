# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0011_auto_20180921_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='PyConCharlaProposal',
            fields=[
                ('pycontalkproposal_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pycon.PyConTalkProposal')),
            ],
            options={
                'verbose_name': 'PyCon Charlas proposal',
            },
            bases=('pycon.pycontalkproposal',),
        ),
    ]
