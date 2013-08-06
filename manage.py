#!/usr/bin/env python
import os
import sys

# On the server, we're started with a command like
#
#   VENV/bin/python manage.py run_gunicorn -c path/to/gunicorn_config.py
#
# so it's up to manage.py to pick what Django settings to use.

if __name__ == "__main__":
    if 'IS_PRODUCTION' in os.environ:
        # We're on server

        def truish(env_value):
            # 'true' or 'false' will be in the env
            return env_value.lower() == 'true'

        if truish(os.environ['IS_PRODUCTION']):
            os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                                  "pycon.settings.production")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                                  "pycon.settings.staging")

    elif 'test' in sys.argv:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "pycon.settings.test")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "pycon.settings.default")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
