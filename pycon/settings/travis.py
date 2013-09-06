# Settings file for Travis
# uses common test settings, then overrides for Travis

from .test import *

# Travis - PostgreSQL is started on boot, binds to 127.0.0.1 and requires
# authentication with "postgres" user and no password.
DATABASES['default'].update(
    {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # if you change DB name here, also change it in .travis.yml
        "NAME": "pycon2014",
        'HOST': '127.0.0.1',
        "USER": "postgres",
        "PASSWORD": "",
    }
)
