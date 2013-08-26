# Top settings file for development
from .base import *

COMPRESS_ENABLED = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['localhost', '0.0.0.0']

# Including a default secret key since this is just for development
SECRET_KEY = env_or_default('SECRET_KEY', u'dipps!+sq49#e2k#5^@4*^qn#8s83$kawqqxn&_-*xo7twru*8')
