# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0011_proposal_created_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalbase',
            name='additional_notes',
            field=models.TextField(help_text='Anything else you would like to share with the committee:<br> <b>Please do not submit any personally identifiable information.</b> The initial round of reviews are annonymous, and this field will visible to reviewers.<br> Speaker public speaking experience.<br> Speaker subject matter experience.<br> Have the speaker(s) given this presentation before elsewhere?<br> Links to recordings, slides, blog posts, code, or other material. <br> Specific needs or special requests \u2014 accessibility, audio (will you need to play pre-recorded sound?), or restrictions on when your talk can be scheduled.', blank=True),
        ),
    ]
