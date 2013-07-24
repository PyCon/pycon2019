# -*- coding: utf-8 -*-
from .base import *

# This will be imported by a settings file on the server,
# then the server file will override just the things that can only be
# known at deployment time, like some paths, the database,
# etc.

# From address for staging - use our development list
DEFAULT_FROM_EMAIL = 'pycon@caktusgroup.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Yes, send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

COMPRESS_ENABLED = True

from django.utils.log import DEFAULT_LOGGING
LOGGING = DEFAULT_LOGGING.copy()

LOGGING['filters'].update(
    {
        'static_fields': {
            '()': 'pycon.logfilters.StaticFieldFilter',
            'fields': {'deployment': 'pycon', 'environment': 'staging'},
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
            # Host is set on server since it's semi-secret
            #'host': GRAYLOG_HOST,
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
