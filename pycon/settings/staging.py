# Staging settings
from .server import *

# From address for staging - use our development list
DEFAULT_FROM_EMAIL = 'pycon@caktusgroup.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
FINANCIAL_AID_WEEKLY_REPORT_EMAIL = ['ewdurbin@gmail.com']

LOGGING['filters']['static_fields']['fields']['environment'] = 'staging'

ALLOWED_HOSTS = [
    'staging-pycon.python.org',
]
