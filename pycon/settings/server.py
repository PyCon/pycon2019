# Common settings for deployed servers
# Will be imported by staging.py, production.py, etc.,
# and some settings possibly overridden.
import socket

from .base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ['DB_NAME'],
        "USER": os.environ['DB_USER'],
        "PASSWORD": os.environ['DB_PASSWORD'],
        "HOST": os.environ['DB_HOST'],
        "PORT": os.environ['DB_PORT'],
    }
}

ALLOWED_HOSTS = [
    '.pycon.org',
    '.python.org',
    'staging-pycon.python.org',
    socket.getfqdn(),
]

SECRET_KEY = os.environ['SECRET_KEY']

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

MEDIA_ROOT = os.environ['MEDIA_ROOT']

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
            'host': os.environ['GRAYLOG_HOST'],
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

# Add Google OAuth2
AUTHENTICATION_BACKENDS[1:1] = ["social_auth.backends.google.GoogleOAuth2Backend",]

# To get the Google OAuth2 Client ID and Secret:
#
# (1) Login to google with some account you control
# (2) Go to https://console.developers.google.com/project
# (3) Create a project, give it some name (e.g. Pycon Web Site, or Pycon Staging Web Site)
# (4) Wait until the page says the project has been created
# (5) The project will open in the dev console
# (6) On the left, select "APIs & auth"/"Credentials"
# (7) Under OAuth, click "Create new Client ID" (don't worry, it's OAuth2)
# (8) Select application type "Web application"
# (9) Enter a Product Name on the consent Screen page and click Save
# (10) In the Create Client ID popup, select
#     Application type:  Web application
#     Authorized JS origins: Your site base URL (e.g. https://staging-pycon.python.org, not
#       https://staging-pycon.python.org/2016/;  https://example.com or
#       http://local.pycon.org:8000, NOT https://example.com/foo/bar or
#       http://local.pycon.org:8000/2016/)
#     Authorized redirect URIs: Should be the same base URL, plus
#       YYYY/account/social/complete/google-oauth2/ - e.g.
#       https://staging-pycon.python.org/2016/account/social/complete/google-oauth2/
# (11) Copy the displayed client ID and client secret

GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')
