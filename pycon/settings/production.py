# Production settings
from .server import *

# From address for production
DEFAULT_FROM_EMAIL = "PyCon 2014 <no-reply@us.pycon.org>"
SERVER_EMAIL = DEFAULT_FROM_EMAIL

LOGGING['filters']['static_fields']['fields']['environment'] = 'production'

ALLOWED_HOSTS = [
    'us.pycon.org',
]
