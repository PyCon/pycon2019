# -*- coding: utf-8 -*-
# base settings - imported by other settings files, then overridden

import os.path
import posixpath

from django.core.urlresolvers import reverse_lazy


def env_or_default(NAME, default):
    return os.environ.get(NAME, default)


# Top level of our source / repository
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir, os.pardir))
# Symposion package
PACKAGE_ROOT = os.path.join(PROJECT_ROOT, "symposion")

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env_or_default("DB_NAME", "pycon2014"),
        "USER": env_or_default("DB_USER", ""),
        "PASSWORD": env_or_default("DB_PASSWORD", ""),
        "HOST": env_or_default("DB_HOST", ""),
        "PORT": env_or_default("DB_PORT", ""),
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

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
USE_I18N = True

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('fr', gettext('French')),
)

LOCALE_PATHS = [os.path.join(PROJECT_ROOT, "locale")]

# Absolute path to the directory that holds media - this is files uploaded
# by users, such as attachments.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = env_or_default("MEDIA_ROOT", os.path.join(PROJECT_ROOT, "site_media", "media"))

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

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

MIDDLEWARE_CLASSES = [
    "djangosecure.middleware.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # LocaleMiddleware must follow session middleware and cache middleware,
    # and precede commonmiddleware
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
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
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",

    # external
    "compressor",
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
    "selectable",

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
    "pycon.finaid",
    "pycon.pycon_api",
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
DEFAULT_FROM_EMAIL = "PyCon 2014 <no-reply@us.pycon.org>"

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {
    # "SETTING_NAME": (default_value, "help text")
    "CTE_SECRET": ("", "Shared secret for CTE integration"),
    "REGISTRATION_URL": ("", "URL for registration"),
    "SHOW_LANGUAGE_SELECTOR": (False, "Show language selector on dashboard"),
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
    "lightning-talk": "pycon.forms.PyConLightningTalkProposalForm",
}

USE_X_ACCEL_REDIRECT = False

MARKEDIT_DEFAULT_SETTINGS = {
    'preview': 'below',
    'toolbar': {
        'backgroundMode': 'dark',
    }
}

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

# Is somebody clobbering this?  We shouldn't have to set it ourselves,
# but if we don't, gunicorn's django_wsgi blows up trying to configure
# logging with an empty dictionary.
from django.utils.log import DEFAULT_LOGGING
LOGGING = DEFAULT_LOGGING
