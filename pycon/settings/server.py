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

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

ADMINS = (
    ('Ernest W. Durbin III', 'ewdurbin@gmail.com'),
)
MANAGERS = ADMINS

# Yes, send email
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
CELERY_EMAIL_BACKEND = 'email_log.backends.EmailBackend'
EMAIL_LOG_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env_or_default("EMAIL_HOST", "")

DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

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
    }
)
LOGGING['loggers'].update(
    {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'pycon': {
            # mail_admins will only accept ERROR and higher
            'handlers': ['mail_admins'],
            'level': 'WARNING',
        },
        'symposion': {
            # mail_admins will only accept ERROR and higher
            'handlers': ['mail_admins'],
            'level': 'WARNING',
        }
    }
)

# Keep sessions in cache
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = 'session'

# Caching
# Celery will use Redis DB 0 for itself.
# General caching will use Redis DB 1.
# Session caching will use Redis DB 2 (so we can clear general cache without
# killing everyone's sessions.)
INSTALLED_APPS.append('redis_cache')
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            'localhost:6379',
        ],
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': 2,
        },
    },
    SESSION_CACHE_ALIAS: {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            'localhost:6379',
        ],
        'OPTIONS': {
            'DB': 2,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': 2,
        },
    },
}

# Use the caching template loader around whatever template loaders we've
# previously configured
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)
