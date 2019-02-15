# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pycon', '0014_auto_20190130_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='PyConRoomSharingOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arrive', models.DateField()),
                ('depart', models.DateField()),
                ('contact_info', models.CharField(max_length=128)),
                ('additional_info', models.CharField(max_length=512)),
                ('approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='room_sharing_offer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PyConRoomSharingRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arrive', models.DateField()),
                ('depart', models.DateField()),
                ('contact_info', models.CharField(max_length=128)),
                ('additional_info', models.CharField(max_length=512)),
                ('approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='room_sharing_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
