Registration
============

The homepage template utilizes a configurable item to display information
about conference registration. Go to
``/YEAR/admin/constance/config/`` and set ``REGISTRATION_STATUS`` to either
``soon``, ``open``, or ``closed``. If the value is an empty string or a value
other than the three valid entries, the homepage template will not include any
specific registration status information or link. If other valid states are
required, the homepage template will have to be modified accordingly.

The registration link (to actually register for the conference) just
goes to a page that uses an iframe to wrap the real registration site,
provided by a vendor.

There are a couple of configuration items that need to be agreed with
the vendor each year, a shared secret and a URL. These should then be
configured using the admin in the ``constance`` app. Go to
``/YEAR/admin/constance/config/`` and set ``CTE_SECRET`` to this year's shared
secret and ``REGISTRATION_URL`` to this year's URL.

When ready to open up registration, make sure the vendor is ready, then put a
link on the front page that goes to the URL named "registration_login", e.g.::

    <a href="{% url 'registration_login' %}">Register!</a>


Tutorial Registration Data
--------------------------

Once the Schedule has been set, and Tutorials are open for registration, a
management command that consumed registration data from the registration
provider can be placed on a cron job for periodic updates.

One must configure the URL of the external CSV report to be consumed.  These
should be configured using the admin in the ``constance`` app. Got to
``/YEAR/admin/constance/config`` and set ``CTE_TUTORIAL_DATA_URL`` to this
year's URL.

Once this is set, running the command job will update the Tutorial registrants
via consumed emails, as well as set the max attendees for the Tutorial::

    python manage.py update_tutorial_registrants
