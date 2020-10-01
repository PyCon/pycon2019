
=====================
 PyCon 2019 Web Site
=====================

Built by the Python Community atop an amazing Django web framework. 

Rather than use this as the basis for your conference site directly, you should
instead look at https://github.com/pinax/symposion which was designed for reuse.

PyCon 2019 is built on top of Pinax Symposion but may have customizations that
will just make things more difficult for you.

Installation instructions are in this README.  There's more documentation
at https://readthedocs.org/projects/pycon/.

Build status for develop branch:

.. image:: https://travis-ci.org/PyCon/pycon.svg?branch=develop
    :target: https://travis-ci.org/PyCon/pycon

Running the PyCon site locally
------------------------------

Before you get started, you'll need a Docker environment, and docker-compose
available, see https://www.docker.com/community-edition for the easiest way
to get that setup for your platform!

Developers can easily run the PyCon web application inside an isolated 
environemnt by using `Docker`_.  Once you have Docker and Docker Compose
installed on your computer, simply check out this project from GitHub
and spin up the site::


    $ git clone https://github.com/PyCon/pycon.git
    $ cd pycon
    $ make up

On this first call to ``up`` that creates the containers, ``make``
will go ahead and automatically perform all of the provisioning steps
that the application needs.  You can later reset the environment using
``make reset``.  Bootstrapping may take a few minutes to
complete, since it downloads Django and all of the libraries it needs.

When ``docker-compose`` finishes, the PyCon application is running with
some sample content!

Finally, you should see the development version of the PyCon web site
when you visit ``http://localhost:8000/`` in your browser!

Two logins are created during the automated setup!

To login as a Django superuser, use the email address ``admin@example.com``
and the password ``None``.

To login as a general user, use the email address ``user@example.com`` and
the password ``None``.

.. _Docker: https://docs.docker.com/compose/install/

Running the PyCon web site in production
----------------------------------------

* You will want to run the application on an Ubuntu 12.04 or 14.04 host.

* Create a new virtualenv and activate it::

    $ virtualenv env/pycon
    $ . env/pycon/bin/activate

* Install the requirements for running and testing locally::

    $ pip install --trusted-host dist.pinaxproject.com -r requirements/project.txt

* Copy ``pycon/settings/local.py-example`` to ``pycon/settings/local.py``.
* Edit ``pycon/settings/local.py`` according to the comments. Note that you
  *will* have to edit it; by default everything there is commented out.

* If you have ssh access to the staging server, copy the database and media::

    $ fab staging get_db_dump:pycon
    $ fab staging get_media

  Change ``pycon`` in that first command to the name of your local database.

  If you get Postgres authorization errors when trying the get_db_dump,
  find another developer who has access already and copy the ~/.pgpass
  file from their account on that server to your own account; it has the
  userids and passwords for the databases.

* Otherwise, ask someone for help. We don't have a good way currently to
  get a new system running from scratch.

* Create a user account::

    $ ./manage.py createsuperuser

* Edit ``pycon/settings/local.py`` to make sure DEBUG=False.
* Add an appropriate ALLOWED_HOSTS setting (https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-ALLOWED_HOSTS)
* Install ``lessc`` (Go to http://lesscss.org and search for "Server-side usage")
* Pre-compress everything by running::

    python manage.py compress --force

  That will write compressed css and js files under site_media
* Gather the static files::

    python manage.py collectstatic --noinput

* Arrange to serve the site_media directory as ``/2018/site_media/whatever``.
  E.g. ``site_media/foo.html`` would be at ``/2018/site_media/foo.html``.
* Arrange to serve the wsgi application in ``symposion/wsgi.py`` at ``/``, running
  with the same virtualenv (or equivalent).  It will only handle URLs
  starting with ``/2018`` though, so you don't have to pass it any other requests.

To run tests
------------

Tests won't run from `/vagrant` inside the vagrant system due to shortcomings
of the way Vagrant makes the host system's files available there.  It's probably
simplest to just do development directly on any Ubuntu 14 system.


::

    python manage.py test

or try running `make test` or `tox`.  (Yes, we have too many ways to run tests.)

Also, Travis (https://travis-ci.org/PyCon/pycon) automatically runs the tests against pull requests.

More documentation
------------------

There's more documentation under ``docs/``.

LICENSE
------------------
.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
