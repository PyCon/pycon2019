Financial Aid
=============

Settings
--------

Create a FINANCIAL_AID setting in Django settings. It should be a dictionary.
Values can include:

    email
        The email address that messages related to financial aid come from,
        and that users should email with questions. Defaults to
        ``pycon-aid@pycon.org``.

Add the context processor:

    TEMPLATE_CONTEXT_PROCESSORS = [
        ...
        "pycon.finaid.context_processors.financial_aid",
        ...
    ]

To enable applications, use the admin to create new
FinancialAidApplicationPeriod records with the desired start
and end dates.


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
