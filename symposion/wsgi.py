# IMPORTANT NOTE: wsgi.py is not being used for staging or production.
# They use "manage.py run_gunicorn ..." with nginx in front as proxy
# and static file server.

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycon.settings.dev")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
