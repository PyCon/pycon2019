import os
import urlparse

from .settings import *

DEBUG = {"dev": True}.get(os.environ["GONDOR_INSTANCE"], False)
TEMPLATE_DEBUG = DEBUG

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": {
                "postgres": "django.db.backends.postgresql_psycopg2"
            }[url.scheme],
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }

if "GONDOR_REDIS_URL" in os.environ:
    urlparse.uses_netloc.append("redis")
    url = urlparse.urlparse(os.environ["GONDOR_REDIS_URL"])
    CACHES = {
        "default": {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": "%s:%s" % (url.hostname, url.port),
            "OPTIONS": {
                "DB": 0,
                "PASSWORD": url.password,
                "PARSER_CLASS": "redis.connection.HiredisParser"
            },
        },
    }

SITE_ID = 1 # set this to match your Sites setup

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "media")
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "static")

ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

FILE_UPLOAD_PERMISSIONS = 0640

SENTRY_DSN = os.environ.get("GONDOR_SENTRY_DSN")

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 0  # 15768000  # @@@ Set this to the Larger Value Once We Are Sure this Works
SECURE_FRAME_DENY = True
#SECURE_CONTENT_TYPE_NOSNIFF = True  # @@@ This would be more secure. But I'm not entirely sure of the ramifications

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = "PYCON2013"

USE_X_ACCEL_REDIRECT = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "propagate": True,
        },
    }
}

METRON_SETTINGS = {
    "google": {
        1: os.environ.get("GONDOR_ANALYTICS_KEY"),
    }
}

DEFAULT_FROM_EMAIL = "PyCon 2014 <no-reply@us.pycon.org>"

if "GONDOR_SENDGRID_USER" in os.environ:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.environ["GONDOR_SENDGRID_USER"]
    EMAIL_HOST_PASSWORD = os.environ["GONDOR_SENDGRID_PASSWORD"]
    EMAIL_USE_TLS = True
