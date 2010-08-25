============================
PyCon US website by Eldarion
============================

This repository stores the PyCon US website developed by Eldarion. This
project is open source and the license can be found in LICENSE.


Installation
============

To get setup with pycon code you must have the follow installed:

 * Python 2.5+
 * virtualenv 1.4.7+
 * C compiler (for PIL)

Setting up environment
----------------------

Create a virtual environment where pycon dependencies will live::

    $ virtualenv --no-site-packages pycon
    $ source pycon/bin/activate
    (pycon)$

Install pycon project dependencies::

    (pycon)$ pip install -r requirements/project.txt

If you are setting up a production environment use
``requirements/production.txt`` instead.

Setting up the database
-----------------------

This will vary for production and development. By default the project is set
up to run on a SQLite database. If you are setting up a production database
see the Configuration section below for where to place settings and get the
database running. Now you can run::

    (pycon)$ python manage.py syncdb
    (pycon)$ python manage.py loaddata fixtures/initial_{wakawaka,boxes}.json

The wakawaka fixtures will require a user to exist before being ran. During
syncdb it is worth it to make a superuser account which can then be used for
making other users staff/superusers after they sign up.

Running a web server
--------------------

In development you should run::

    (pycon)$ python manage.py runserver

@@@ TODO: not sure what will be used for deployment yet. This project comes
with a ``deploy/pinax.wsgi`` which can be used with mod_wsgi and showcase how
to setup the WSGI environment if another mechanism is chosen.

Sending mail/notification
-------------------------

All mail and some notification are queued in the database to be sent later. In
a future version of Pinax this will made much more configurable. It is best
to setup a cron job to run these two commands every minute::

    (pycon)$ python manage.py send_mail
    (pycon)$ python manage.py emit_notices

And this one every 10–20 minutes::

    (pycon)$ python manage.py retry_deferred

More information can be found in `Pinax deployment documentation`_.

.. _Pinax deployment documentation: http://pinaxproject.com/docs/dev/deployment.html#sending-mail-and-notices

Configuration
=============

You can create a ``local_settings.py`` file alongside ``settings.py`` to
override any setting that may be environment/instance specific. This file is
ignored in ``.gitignore``.


Issues
======

If you find an issue with this code base you are welcome to e-mail us at
development@eldarion.com.