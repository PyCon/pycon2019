# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0010_rename_special_event_to_scheduled_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edusummittalkproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='/2019/speaking/recording/' target='_blank'>PyCon 2019 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pyconlightningtalkproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='/2019/speaking/recording/' target='_blank'>PyCon 2019 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pyconopenspaceproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='/2019/speaking/recording/' target='_blank'>PyCon 2019 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pyconposterproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='/2019/speaking/recording/' target='_blank'>PyCon 2019 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pycontalkproposal',
            name='outline',
            field=models.TextField(help_text='The \u201coutline\u201d is a skeleton of your talk that is as detailed as possible, including rough timings or estimates for different sections. If requesting a 45 minute slot, please describe what content would appear in the 45 minute version but not a 30 minute version, either within the outline or in a paragraph at the end.<br> <br> <i>Committee note:</i> The outline is extremely important for the program committee to understand what the content and structure of your talk will be. The timings/percentages help us compare multiple talks that might have a similar abstract. We know that they are estimates and only capture your view at this moment in time and are likely to change before PyCon. We hope that writing the outline is helpful to you as well, to organize and clarify your thoughts for your talk! The outline will not be shared with conference attendees.<br> <br> If there\u2019s too much to your topic to cover even in 45 minutes, you may wish to narrow it down. Alternatively, consider submitting a 3-hour PyCon tutorial instead. If you plan to do live coding during your talk, please describe your backup plan in case the live coding fails (for whatever reason). Suggestions include a pre-recorded video, or slides to replace the live coding.'),
        ),
        migrations.AlterField(
            model_name='pycontalkproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='/2019/speaking/recording/' target='_blank'>PyCon 2019 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pycontutorialproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='/2019/speaking/recording/' target='_blank'>PyCon 2019 Recording Release</a> for details."),
        ),
    ]
