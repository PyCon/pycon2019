Special Events
==============

Special events are events that don't fit into the other categories.

To create one, use the Django admin (``/YYYY/admin``) and look for
*PyCon Special Events*.  When adding one, all fields are required
except for the "Published" checkbox, which defaults to False. Set
Published to True if you want to be able to view the event on the
web site.

Showing events on the website
-----------------------------

Make sure the "Published" field is set to True in the admin.

When editing the event in the admin, use the "View on site"
button in the top right to see the event's page. Copy its URL
from your browser's address bar.

You can use the URL in links on other pages as-is.

Add events to Menus
-------------------

To add an event to the site menus, go to the Django admin, find the
site tree called "main" and open it, then add a new item. Set the
URL to the event's URL, minus the hostname part - e.g. if the
full URL is ``https://us.pycon.org/2018/scheduled_events/bigbash/``,
just include ``/2018/scheduled_events/bigbash/``.
