# This is used for staging & production
import os
import sys

settings = None
if 'IS_PRODUCTION' in os.environ:
    # We're on a deployed server if the var "IS_PRODUCTION" exists, with any value.
    # The value tells us if we're production or staging, so we
    # can use the appropriate settings. The value is set by Chef
    # using Ruby, so True is spelled 'true'.
    if os.environ['IS_PRODUCTION'] == 'true':
        settings = "production"
    else:
        settings = "staging"
elif 'test' in sys.argv:
    # Running tests - use test-specific settings
    settings = "test"
else:
    # Try to load pycon.settings.local and fail with a useful message
    # if that doesn't work.
    settings = "default"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycon.settings.%s" % settings)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
