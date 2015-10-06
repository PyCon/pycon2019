# Settings file for running tests locally
# See also travis.py

from .base import *  # noqa

# Use nose and its test runner so we only run our own tests and not those
# of every app installed.
INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Debug logs during testing are WAY too verbose
NOSE_ARGS = ['--nologcapture']

# Turn compress on to be closer to production env
COMPRESS_ENABLED = True

# Including a default secret key since this is just for test
SECRET_KEY = env_or_default('SECRET_KEY', u'dipps!+sq49#e2k#5^@4*^qn#8s83$kawqqxn&_-*xo7twru*8')

# Using sqlite in memory speeds things up even more, but that's getting
# pretty far from production. I don't think it's worth the risk.
# DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": ":memory:",
#    }
# }
