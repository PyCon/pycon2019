PyCon 2015 website being built by Caktus Consulting Group, based on symposion.

Rather than use this as the basis for your conference site directly, you should
instead look at https://github.com/pinax/symposion which was designed for reuse.

PyCon 2015 is built on top of Pinax Symposion but may have customizations that
will just make things more difficult for you.

Installation instructions are in this README.  There's more documentation
at https://readthedocs.org/projects/pycon/.

To get running locally
----------------------

* First, if you're not on Ubuntu 12.04 or 14.04, you might need to do the following in
  a virtual machine that is running one of them.  You can use the provided
  Vagrantfile to create one running Ubuntu 12.04 and install some of the prerequisites::

    $ vagrant up

  That'll have the current local directory mounted internally as /vagrant.
  Ssh into the vagrant system and change directories to /vagrant::

    $ vagrant ssh
    $ cd /vagrant

  and then continue working there with the following instructions.

* If you are already on an Ubuntu system (12.04 or 14.04), you can skip using vagrant and
  just continue on from here.

* Create a new virtualenv and activate it::

    $ virtualenv env/pycon
    $ . env/pycon/bin/activate

* Install the requirements for running and testing locally::

    $ pip install --trusted-host dist.pinaxproject.com -r requirements/dev.txt

  (For production, install -r requirements/project.txt).

* Copy ``pycon/settings/local.py-example`` to ``pycon/settings/local.py``.
* Edit ``pycon/settings/local.py`` according to the comments. Note that you
  `will` have to edit it; by default everything there is commented out.

* If you have ssh access to the staging server, copy the database and media::

    $ fab staging get_db_dump:pycon2016
    $ fab staging get_media

  Change ``pycon2016`` in that first command to the name of your local database.

* Otherwise, ask someone for help. We don't have a good way currently to
  get a new system running from scratch.

* Create a user account::

    $ ./manage.py createsuperuser

* Run local server, binding to all IP addresses, and using port 8000::

    python manage.py runserver 0.0.0.0:8000

* Now you should be able to visit the running site from your host system's browser
  at `http://localhost:8000`.  (Vagrant is fowarding port 8000 from the vagrant
  system to the host system.)


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

Tests won't run from `/vagrant` inside the vagrant system due to shortcomings
of the way Vagrant makes the host system's files available there.  It's probably
simplest to just do development directly on any Ubuntu 14 system.


::

    python manage.py test

or try running `make test` or `tox`.  (Yes, we have too many ways to run tests.)

More documentation
------------------

There's more documentation under ``docs/``.
