PyCon 2015 website being built by Caktus Consulting Group, based on symposion.

Rather than use this as the basis for your conference site directly, you should
instead look at https://github.com/pinax/symposion which was designed for reuse.

PyCon 2015 is built on top of Pinax Symposion but may have customizations that
will just make things more difficult for you.

Installation instructions are in this README.  There's more documentation
at https://readthedocs.org/projects/pycon/.

To get running locally
----------------------

* First, if you're not on Ubuntu 12.04, you might need to do the following in
  a virtual machine that is running Ubuntu 12.04.  You can use the provided
  Vagrantfile to create one and install some of the prerequisites::

    $ vagrant up

  That'll have the current local directory mounted internally as /vagrant, but
  it's not a full-featured file system so tox won't work right. What I did was
  copy the files to the user's home directory::

    $ vagrant ssh
    [now in vagrant system, logged in as vagrant, with sudo privs]
    $ cd /vagrant
    $ rsync -avz * ~
    $ cd ~

  and then continue working there with the following instructions.

* Create a new virtualenv and activate it::

    $ virtualenv env/pycon
    $ . env/pycon/bin/activate

* Install the requirements for running and testing locally::

    $ pip install --trusted-host dist.pinaxproject.com -r requirements/dev.txt

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

* Otherwise, create a new empty database::

    $ createdb pycon2015
    $ ./manage.py syncdb

* Run local server::

    python manage.py runserver

* Run tests::

    $ tox

 or

    $ make test


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
