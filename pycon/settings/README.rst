Settings files for Pycon project
================================

Each environment has its own settings file. They first import ``base.py``,
then override as needed.

``manage.py`` will default to looking for settings in pycon/settings/local.py,
which should not be in version control.
That file would import * from the appropriate environmental settings file,
and could then override if needed (should be minimal).  E.g.::

    # pycon/settings/local.py for local development system
    from .dev import *

    MIDDLEWARE_CLASSES += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]

Whereas on a server::

    # pycon/settings/local.py on staging server
    from .staging import *

    DATABASES['default']['password'] = TOP_SECRET_PASSWORD
    LOGGING = COMPLICATED SERVER LOGGING CONFIG

Alternatively, you can start Django with ``--settings`` used or
``DJANGO_SETTINGS_MODULE`` set correctly for the desired environment
to load that environment's own settings file if you don't need to override
anything.

``base`` has some minimal, conservative settings:

* Database is "pyconYYYY" using Postgres.
* DEBUG is False.
* COMPRESS_ENABLED is False.
* Email handler set to console.
* Logging explicitly set to the Django defaults.
* SECRET_KEY is not set.

Other settings files:

* production - for production
* staging - for staging
* test - for local testing
* travis - for Travis testing
* dev - for local development
