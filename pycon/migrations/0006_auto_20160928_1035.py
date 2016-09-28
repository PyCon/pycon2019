# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0005_edusummittalkproposal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pycontalkproposal',
            name='perceived_value',
        ),
        migrations.RemoveField(
            model_name='pycontalkproposal',
            name='thunderdome_group',
        ),
        migrations.AlterField(
            model_name='pycontalkproposal',
            name='audience',
            field=models.TextField(help_text='1\u20132 paragraphs that should answer three questions: (1) Who is this talk for? (2) What background knowledge or experience do you expect the audience to have? (3) What do you expect the audience to learn or do after watching the talk?<br> <br> <i>Committee note:</i> The \u201cAudience\u201d section helps the program committee get a sense of whether your talk is geared more at novices or experienced individuals in a given subject. (We need a balance of both lower-level and advanced talks to make a great PyCon!) It also helps us evaluate the relevance of your talk to the Python community.', verbose_name='Who and Why (Audience)'),
        ),
        migrations.AlterField(
            model_name='pycontalkproposal',
            name='duration',
            field=models.IntegerField(default=1, help_text='<i>Committee note:</i> There are far fewer 45 minute slots available than 30 minute slots, so not every accepted talk that requests a longer slot may be able to get it. If you select a 45 minute slot, please indicate in your outline (below) what content could be cut \u2014 if possible \u2014 for a 30 minute version.', choices=[(0, 'No preference'), (1, 'I prefer a 30 minute slot'), (2, 'I prefer a 45 minute slot')]),
        ),
        migrations.AlterField(
            model_name='pycontalkproposal',
            name='outline',
            field=models.TextField(help_text='The \u201coutline\u201d is a skeleton of your talk that is as detailed as possible, including rough timings for different sections. If requesting a 45 minute slot, please describe what content would appear in the 45 minute version but not a 30 minute version, either within the outline or in a paragraph at the end.<br> <br> <i>Committee note:</i> The outline is extremely important for the program committee to understand what the content and structure of your talk will be. We hope that writing the outline is helpful to you as well, to organize and clarify your thoughts for your talk! The outline will <b>not</b> be shared with conference attendees.<br> <br> If there\u2019s too much to your topic to cover even in 45 minutes, you may wish to narrow it down. Alternatively, consider submitting a 3-hour PyCon tutorial instead.'),
        ),
    ]
