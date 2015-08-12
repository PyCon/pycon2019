# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Google OpenID auth has been turned off, so any associations that
users had to their Google accounts via Google OpenID are now useless.
Just remove them.
"""

from django.db import migrations


def no_op(apps, schema_editor):
    pass


def remove_old_google_openid_auths(apps, schema_editor):
    UserSocialAuth = apps.get_model('social_auth', 'UserSocialAuth')
    db_alias = schema_editor.connection.alias

    UserSocialAuth.objects.using(db_alias).filter(provider='google').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_old_google_openid_auths, no_op),
    ]
