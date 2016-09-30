# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0006_auto_20160928_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edusummittalkproposal',
            name='category',
            field=models.ForeignKey(blank=True, to='pycon.PyConProposalCategory', null=True),
        ),
        migrations.AlterField(
            model_name='pyconlightningtalkproposal',
            name='category',
            field=models.ForeignKey(blank=True, to='pycon.PyConProposalCategory', null=True),
        ),
        migrations.AlterField(
            model_name='pyconopenspaceproposal',
            name='category',
            field=models.ForeignKey(blank=True, to='pycon.PyConProposalCategory', null=True),
        ),
        migrations.AlterField(
            model_name='pyconposterproposal',
            name='category',
            field=models.ForeignKey(blank=True, to='pycon.PyConProposalCategory', null=True),
        ),
        migrations.AlterField(
            model_name='pycontalkproposal',
            name='category',
            field=models.ForeignKey(blank=True, to='pycon.PyConProposalCategory', null=True),
        ),
        migrations.AlterField(
            model_name='pycontutorialproposal',
            name='category',
            field=models.ForeignKey(blank=True, to='pycon.PyConProposalCategory', null=True),
        ),
    ]
