# Production settings
from .server import *

# From address for production
DEFAULT_FROM_EMAIL = "PyCon %s <no-reply@us.pycon.org>" % CONFERENCE_YEAR
FINANCIAL_AID_EMAIL = "pycon-aid@python.org"
ORGANIZERS_EMAIL = 'pycon-organizers@python.org'
REGISTRATION_EMAIL = 'pycon-reg@python.org'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
SPONSORSHIP_EMAIL = 'pycon-sponsors@python.org'
THEME_CONTACT_EMAIL = 'pycon-reg@python.org'

LOGGING['filters']['static_fields']['fields']['environment'] = 'production'

ALLOWED_HOSTS = [
    'us.pycon.org',
]
