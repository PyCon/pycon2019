API
===

There's a very basic API.

Authentication
--------------

To use the API requires an authentication key. Admins can add records
to the pycon.APIAuth table and then give the randomly generated key to
a user.  They can also set a record to disabled (or just delete it) to
revoke access.

When calling the API, users should add a request header ``HTTP_X_API_KEY``
whose value is the key that an admin gave them.

Proposal data
--------------

The proposal data methods allow associating an arbitrary blob of text
(perhaps JSON) with a proposal, and retrieving it later.

.. autofunction:: pycon.pycon_api.views.set_proposal_data
.. autofunction:: pycon.pycon_api.views.get_proposal_data
.. autofunction:: pycon.pycon_api.views.proposal_detail

IRC logs
--------

The IRC logs methods allow associating IRC log lines with a proposal,
and retrieving them later.

The API tracks timestamps to the microsecond (if the database supports
it), but be warned that the Django admin will lose the microseconds if
you edit a log line there.

.. autofunction:: pycon.pycon_api.views.set_irc_logs
.. autofunction:: pycon.pycon_api.views.get_irc_logs
.. autofunction:: pycon.pycon_api.views.proposal_irc_logs


Presentation URLs
-----------------

The presentation URLs method allows setting a talk's video,
slides, and assets URLs.

.. autofunction:: pycon.pycon_api.views.set_talk_urls
