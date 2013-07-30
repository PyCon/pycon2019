# Top settings file for development
from .base import *

COMPRESS_ENABLED = False
DEBUG = True
ALLOWED_HOSTS = ['localhost', '0.0.0.0']

# Including a secret key since this is just for development
SECRET_KEY = u'dipps!+sq49#e2k#5^@4*^qn#8s83$kawqqxn&_-*xo7twru*8'
