# Top settings file for development
from .base import *

# Assume Postgres and ``pycon2014`` as the database. Developer can override
# in local_settings.py.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "pycon2014",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

COMPRESS_ENABLED = False
DEBUG = True
ALLOWED_HOSTS = ['localhost', '0.0.0.0']

# Including a secret key since this is just for development
SECRET_KEY = u'dipps!+sq49#e2k#5^@4*^qn#8s83$kawqqxn&_-*xo7twru*8'
