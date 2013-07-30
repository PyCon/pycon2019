# Top settings file for running tests locally
# See also travis.py

from .base import *

INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Turn compress on to be closer to production env
COMPRESS_ENABLED = True

# Including a secret key since this is just for development
SECRET_KEY = u'dipps!+sq49#e2k#5^@4*^qn#8s83$kawqqxn&_-*xo7twru*8'
