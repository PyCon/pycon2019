PyCon 2015 website being built by Caktus Consulting Group, based on symposion.

Rather than use this as the basis for your conference site directly, you should
instead look at https://github.com/pinax/symposion which was designed for reuse.

PyCon 2015 is built on top of Pinax Symposion but may have customizations that
will just make things more difficult for you.

Installation instructions are in this README.  There's more documentation
at https://readthedocs.org/projects/pycon/.

To get running locally
----------------------

* Create a new virtualenv and activate it::

    $ virtualenv env/pycon
    $ . env/pycon/bin/activate

* Install the requirements for running and testing locally::

    $ pip install -r requirements/dev.txt

  (For production, install -r requirements/project.txt).

* Copy ``pycon/settings/local.py-example`` to ``pycon/settings/local.py``.
* Edit ``pycon/settings/local.py`` according to the comments. Note that you
  `will` have to edit it; by default everything there is commented out.

* Setup the database::

    $ ./load_fixtures.sh

* Create a user account::

    $ ./manage.py createsuperuser

* If you have ssh access to the staging server, copy the database and media::

    $ fab staging get_db_dump:pycon2015
    $ fab staging get_media

  Change ``pycon2015`` in that first command to the name of your local database.

* Run local server::

    python manage.py runserver

For production
--------------

* Start with instructions above, except:

  * Install requirements from requirements/project.txt instead of requirements/dev.txt
  * Stop when you get to `Run local server`

* Edit ``pycon/settings/local.py`` to make sure DEBUG=False.
* Add an appropriate ALLOWED_HOSTS setting (https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-ALLOWED_HOSTS)
* Install ``lessc`` (Go to http://lesscss.org and search for "Server-side usage")
* Pre-compress everything by running::

    python manage.py compress --force

  That will write compressed css and js files under site_media
* Gather the static files::

    python manage.py collectstatic --noinput

* Arrange to serve the site_media directory as ``/2015/site_media/whatever``.
  E.g. ``site_media/foo.html`` would be at ``/2015/site_media/foo.html``.
* Arrange to serve the wsgi application in ``symposion/wsgi.py`` at ``/``, running
  with the same virtualenv (or equivalent).  It will only handle URLs
  starting with ``/2015`` though, so you don't have to pass it any other requests.

To run tests
------------

::

    python manage.py test

More documentation
------------------

There's more documentation under ``docs/``.
