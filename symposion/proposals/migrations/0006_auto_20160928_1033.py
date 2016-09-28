# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0005_auto_20160912_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalbase',
            name='additional_notes',
            field=models.TextField(help_text='Anything else you would like to share with the committee:<br> Speaker public speaking experience.<br> Speaker subject matter experience.<br> Have the speaker(s) given this presentation before elsewhere?<br> Links to recordings, slides, blog posts, code, or other material. <br> Specific needs or special requests \u2014 accessibility, audio (will you need to play pre-recorded sound?), or restrictions on when your talk can be scheduled.', blank=True),
        ),
        migrations.AlterField(
            model_name='proposalbase',
            name='description',
            field=models.TextField(help_text='1\u20132 paragraphs summing up what the presentation is about. This will appear in the conference program and should help attendees decide whether this presentation is relevant to them. Maximum 400 characters.', max_length=400, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='proposalbase',
            name='title',
            field=models.CharField(help_text='Puns, jokes, or \u201chooks\u201d in titles are okay, but make sure that if all someone knew was the title, they still would have some idea what the presentation is about.', max_length=100),
        ),
    ]
