# -*- coding: utf-8 -*-
# Django settings for account project

import os.path
import posixpath

from django.core.urlresolvers import reverse_lazy


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = False

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "pycon2014",                       # Or path to database file if using sqlite3.
        "USER": "",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Eastern"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# Conference ID and any URL prefixes
CONFERENCE_ID = 1
CONFERENCE_URL_PREFIXES = {
    1: "2014",
}


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media - this is files uploaded
# by users, such as attachments.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/%s/site_media/media/" % CONFERENCE_URL_PREFIXES[CONFERENCE_ID]

# Absolute path to the directory where static files will be gathered
# at deploy time and served from in production.  Should NOT be
# in version control, or contain anything before deploying.
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/%s/site_media/static/" % CONFERENCE_URL_PREFIXES[CONFERENCE_ID]

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PACKAGE_ROOT, "static"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Subdirectory of COMPRESS_ROOT to store the cached media files in
COMPRESS_OUTPUT_DIR = "cache"

# Make this unique, and don't share it with anybody.
SECRET_KEY = "8*br)9@fs!4nzg-imfrsst&oa2udy6z-fqtdk0*e5c1=wn)(t3"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

MIDDLEWARE_CLASSES = [
    "djangosecure.middleware.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "reversion.middleware.RevisionMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "symposion.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "pycon/templates"),
    os.path.join(PACKAGE_ROOT, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "social_auth.context_processors.social_auth_backends",
    "pinax_utils.context_processors.settings",
    "account.context_processors.account",
    "symposion.reviews.context_processors.reviews",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # theme
    # "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",

    # external
    "compressor",
    "debug_toolbar",
    "mailer",
    "django_openid",
    "timezones",
    "metron",
    "easy_thumbnails",
    "account",
    "sitetree",
    "taggit",
    "reversion",
    "biblion",
    "social_auth",
    "djangosecure",
    "raven.contrib.django",
    "constance",
    "constance.backends.database",
    "redis_cache",
    "south",
    "uni_form",
    "gunicorn",

    # symposion
    "symposion.conference",
    "symposion.cms",
    "symposion.boxes",
    "symposion.speakers",
    "symposion.proposals",
    "symposion.reviews",
    "symposion.teams",
    "symposion.schedule",

    # custom
    "markedit",
    "pycon",
    "pycon.sponsorship",
    "pycon.registration",
    "pycon.schedule",
    "pycon.profile",
]

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False
ACCOUNT_CREATE_ON_SAVE = True

AUTHENTICATION_BACKENDS = [
    # Permissions backends
    "symposion.teams.backends.TeamPermissionsBackend",

    # Social Auth Backends
    "social_auth.backends.google.GoogleBackend",
    "social_auth.backends.yahoo.YahooBackend",
    "social_auth.backends.OpenIDBackend",

    # Django User Accounts
    "account.auth_backends.EmailAuthenticationBackend",
]

SOCIAL_AUTH_PIPELINE = [
    "social_auth.backends.pipeline.social.social_auth_user",
    "social_auth.backends.pipeline.user.get_username",
    "symposion.social_auth.pipeline.user.create_user",
    "social_auth.backends.pipeline.social.associate_user",
    "social_auth.backends.pipeline.social.load_extra_data",
    "social_auth.backends.pipeline.user.update_user_details",
]

LOGIN_URL = reverse_lazy("account_login")

ACCOUNT_SIGNUP_REDIRECT_URL = "dashboard"
ACCOUNT_LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_USER_DISPLAY = lambda user: user.get_full_name()

# Need these to be reversed urls, currently breaks if using reverse_lazy
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/2014/dashboard/"
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = "/2014/dashboard/"

SOCIAL_AUTH_ASSOCIATE_BY_MAIL = False

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {
    "CTE_SECRET": ("", "Shared secret for CTE integration"),
}

BIBLION_PARSER = ["symposion.markdown_parser.parse", {}]
BIBLION_SECTIONS = [
    ("general", "General"),
]

SYMPOSION_PAGE_REGEX = r"(([\w-]{1,})(/[\w-]{1,})*)/$"

PROPOSAL_FORMS = {
    "tutorial": "pycon.forms.PyConTutorialProposalForm",
    "talk": "pycon.forms.PyConTalkProposalForm",
    "poster": "pycon.forms.PyConPosterProposalForm",
    "sponsor-tutorial": "pycon.forms.PyConSponsorTutorialForm",
}

USE_X_ACCEL_REDIRECT = False

MARKEDIT_DEFAULT_SETTINGS = {'preview': 'below', }

COMPRESS_PRECOMPILERS = (
   ('text/less', 'lessc {infile} {outfile}'),
)

# Is somebody clobbering this?  We shouldn't have to set it ourselves,
# but if we don't, gunicorn's django_wsgi blows up trying to configure
# logging with an empty dictionary.
from django.utils.log import DEFAULT_LOGGING
LOGGING = DEFAULT_LOGGING

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
