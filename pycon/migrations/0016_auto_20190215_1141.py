# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0015_pyconroomsharingoffer_pyconroomsharingrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pyconroomsharingoffer',
            name='approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='pyconroomsharingoffer',
            name='user',
            field=models.OneToOneField(related_name='room_sharing_offer', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pyconroomsharingrequest',
            name='approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='pyconroomsharingrequest',
            name='user',
            field=models.OneToOneField(related_name='room_sharing_request', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
