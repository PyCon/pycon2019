Financial Aid
=============

Settings
--------

Create a FINANCIAL_AID setting in Django settings. It should be a dictionary.
Values can include:

    start_date
        (datetime object) If set, financial aid applications will not be
        accepted or allowed to be edited before this date.
    end_date
        (datetime object) If set, financial aid applications will not be
        accepted or allowed to be edited after this date.
    email
        The email address that messages related to financial aid come from,
        and that users should email with questions. Defaults to
        ``pycon-aid@pycon.org``.

If neither start_date or end_date is set, applications are closed.

So if you wanted the application period to be July, 2013, you would set:

.. code-block:: python

    import datetime

    FINANCIAL_AID = {
        'start_date': datetime.datetime(2013, 7, 1),
        'end_date': datetime.datetime(2013, 7, 31, 23, 59, 59),
    }


Add the context processor:

    TEMPLATE_CONTEXT_PROCESSORS = [
        ...
        "pycon.finaid.context_processors.financial_aid",
        ...
    ]


Templates
---------

Editing applications
~~~~~~~~~~~~~~~~~~~~

To create or edit an application, the app uses the ``finaid/edit.html``
template. The context provides a ``form`` variable containing the form.
A default template is provided that is customized to work with the Pycon
site and uses ``js/finaid.js`` to hide some of the fields unless some
other inputs have been checked, but the view doesn't care; it just wants
the form submitted.

Email notices
~~~~~~~~~~~~~

The text for many emails comes from templates:

    finaid/email/application_submitted_{subject,body}.txt - Sent to user when
        we receive their application

    finaid/email/application_edited_{subject,body}.txt - Sent to user when
        we receive an edit of their application

    finaid/email/applicant_message_{subject,body}.txt - Sent to reviewers
        when the applicant submits a message on the status page

Subject templates should be a single line.
