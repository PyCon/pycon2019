# Common settings for deployed servers
# Will be imported by staging.py, production.py, etc.,
# and some settings possibly overridden.
import socket

from .base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env_or_default('DB_NAME', ''),
        "USER": env_or_default('DB_USER', ''),
        "PASSWORD": env_or_default('DB_PASSWORD', ''),
        "HOST": env_or_default('DB_HOST', ''),
        "PORT": env_or_default('DB_PORT', ''),
    }
}

ALLOWED_HOSTS = [
    '.pycon.org',
    '.python.org',
    'staging-pycon.python.org',
    socket.getfqdn(),
]

SECRET_KEY = env_or_default('SECRET_KEY', '')

ADMINS = (
    ('Ernest W. Durbin III', 'ewdurbin@gmail.com'),
    ('Caktus Pycon Team', 'pycon@caktusgroup.com'),
)
MANAGERS = ADMINS

# Yes, send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env_or_default("EMAIL_HOST", "")

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# tells Pinax not to serve media through the staticfiles app.
SERVE_MEDIA = False

# yes, use django-compressor on the server
COMPRESS_ENABLED = True

MEDIA_ROOT = env_or_default('MEDIA_ROOT', '')

from django.utils.log import DEFAULT_LOGGING
LOGGING = DEFAULT_LOGGING.copy()

LOGGING['filters'].update(
    {
        'static_fields': {
            '()': 'pycon.logfilters.StaticFieldFilter',
            'fields': {
                'deployment': 'pycon',
                'environment': '?'   # should be overridden
            },
        },
        'django_exc': {
            '()': 'pycon.logfilters.RequestFilter',
        },
    }
)
LOGGING['handlers'].update(
    {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,
            'filters': ['require_debug_false'],
        },
        'sam_gelf': {
            'class': 'graypy.GELFHandler',
            'host': env_or_default('GRAYLOG_HOST', ''),
            'port': 12201,
            'filters': ['static_fields', 'django_exc'],
        }
    }
)
LOGGING['loggers'].update(
    {
        'django.request': {
            'handlers': ['mail_admins', 'sam_gelf'],
            'level': 'ERROR',
            'propagate': True,
        },
        'pycon': {
            # mail_admins will only accept ERROR and higher
            'handlers': ['mail_admins', 'sam_gelf'],
            'level': 'WARNING',
        },
        'symposion': {
            # mail_admins will only accept ERROR and higher
            'handlers': ['mail_admins', 'sam_gelf'],
            'level': 'WARNING',
        }
    }
)
