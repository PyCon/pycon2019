API
===

There's a basic API.

Authentication
--------------

Most calls in the API require an authentication key to use. Admins can add records
to the pycon.APIAuth table using the Django admin and then give the randomly generated key and
secret to a user.  They can also set a record to disabled (or just delete
it) to revoke access.

The user will need to add three headers when calling any API that requires
a key: HTTP_X_API_KEY, HTTP_X_API_SIGNATURE, and HTTP_X_API_TIMESTAMP.

Here's sample code to compute them::

    import datetime
    from calendar import timegm
    from hashlib import sha1
    import pytz


    def get_api_key_headers(api_key, api_secret, uri, method='GET', body=''):
        """Return a dictionary with the additional API key headers."""
        # What time is it now?
        timestamp = timegm(datetime.datetime.now(tz=pytz.UTC).timetuple())

        # Calculate the base string to use for the signature.
        base_string = unicode(''.join((
            api_secret,
            unicode(timestamp),
            method.upper(),
            uri,
            body,
        ))).encode('utf-8')

        # Return a dictionary with the headers to send.
        return {
            'HTTP_X_API_KEY': api_key,
            'HTTP_X_API_SIGNATURE': sha1(base_string).hexdigest(),
            'HTTP_X_API_TIMESTAMP': timestamp,
        }

Return values
-------------

All the APIs that require an API key have pretty consistent return value syntax.
On success, JSON will be returned that looks like::

    {
        'code': 2xx,
        'data': depends on the call
    }

On failure, the response will typically look like::

    {
        'code': 4xx,
        'message': 'some error message'
    }

In all cases, the 'code' in the response body data will be the same as the
HTTP protocol status code that is returned.

The few APIs that don't require an API key are a bit more varied in their behavior.


Proposal APIs
-------------

APIs that are used while considering proposals.

.. autofunction:: pycon.pycon_api.views.proposal_list
.. autofunction:: pycon.pycon_api.views.proposal_detail
.. autofunction:: pycon.pycon_api.views.proposal_irc_logs
.. autofunction:: pycon.pycon_api.views.thunderdome_group_add
.. autofunction:: pycon.pycon_api.views.thunderdome_group_list
.. autofunction:: pycon.pycon_api.views.thunderdome_group_decide

Schedule APIs
-------------

The conference data APIs allow retrieving and updating data about
the schedule and sessions.

.. autofunction:: symposion.schedule.views.schedule_json
.. autofunction:: pycon.schedule.views.session_staff_json
.. autofunction:: pycon.pycon_api.views.set_talk_urls

