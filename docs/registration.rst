Registration
============

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
