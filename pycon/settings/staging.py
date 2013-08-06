# Staging settings
from .server import *

# From address for staging - use our development list
DEFAULT_FROM_EMAIL = 'pycon@caktusgroup.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

LOGGING['filters']['static_fields']['fields']['environment'] = 'staging'
