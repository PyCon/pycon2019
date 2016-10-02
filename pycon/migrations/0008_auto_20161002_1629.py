# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0007_auto_20160930_0834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pycontutorialproposal',
            name='more_info',
        ),
        migrations.RemoveField(
            model_name='pycontutorialproposal',
            name='perceived_value',
        ),
        migrations.AlterField(
            model_name='edusummittalkproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2017/speaking/recording/' target='_blank'>PyCon 2017 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pyconlightningtalkproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2017/speaking/recording/' target='_blank'>PyCon 2017 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pyconopenspaceproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2017/speaking/recording/' target='_blank'>PyCon 2017 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pyconposterproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2017/speaking/recording/' target='_blank'>PyCon 2017 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pycontalkproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2017/speaking/recording/' target='_blank'>PyCon 2017 Recording Release</a> for details."),
        ),
        migrations.AlterField(
            model_name='pycontutorialproposal',
            name='audience',
            field=models.TextField(help_text='1\u20132 paragraphs that should answer three questions: (1) Who is this tutorial for? (2) What background knowledge or experience do you expect students to have? (3) What do you expect students to learn, or to be able to do after attending your tutorial?', verbose_name='Audience'),
        ),
        migrations.AlterField(
            model_name='pycontutorialproposal',
            name='outline',
            field=models.TextField(help_text='Make an outline that lists the topics and activities you will guide your students through over the 3 hours of your tutorial. Provide timings for each activity \u2014 indicate when and for how long you will lecture, and when and for how long students will be tackling hands-on exercises.'),
        ),
        migrations.AlterField(
            model_name='pycontutorialproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text="By submitting your proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2017/speaking/recording/' target='_blank'>PyCon 2017 Recording Release</a> for details."),
        ),
    ]
