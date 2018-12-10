# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0012_updates_to_finaidreviewdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialaidapplication',
            name='application_type',
            field=models.CharField(default=b'general', help_text='Application Classification', max_length=64, verbose_name='Application Type', choices=[(b'general', 'General Applicant'), (b'staff', 'PyCon Staff/Volunteer'), (b'speaker', 'Speaker'), (b'core_dev', 'Python Core Developer'), (b'psf_board', 'PSF Board Member'), (b'outstanding_community_member', 'Outstanding Community Member')]),
        ),
    ]
