Financial Aid
=============

Settings
--------

Create a FINANCIAL_AID setting in Django settings. It should be a dictionary.
Values can include:

    email
        The email address that messages related to financial aid come from,
        and that users should email with questions. Defaults to
        ``pycon-aid@python.org``.


To enable applications, use the admin to create new
FinancialAidApplicationPeriod records with the desired start
and end dates.

Reviewer email to applicants
----------------------------

Reviewers can select one or more applicants on the application list page
and click "Send email".  On the next page, they can enter a subject, pick
a template, and click "Send". Each applicant selected will receive an email
customized for them using the template chosen.

Templates for this function are created and edited in the admin, at e.g.
``/2014/admin/finaid/financialaidemailtemplate/``.

Each template has a name, which is just used to identify the template
here and on the mail sending page, and a body, which uses Django templating
to render the body of each email.

In the template body, you have access to the usual Django template tags,
and some variables that you can access:

* application - a ``FinancialAidApplication`` object. This gives access to a
  lot of useful information from the user's application that can be used in
  your email, e.g.::

      Dear {{ application.user.get_full_name }},

      {% if application.travel_grant_requested %}You requested a travel grant...{% endif %}

* review - a ``FinancialAidReviewData`` object. This gives access to the
  information from the review of the application. E.g.::

      {% if review.hotel_amount %}You are being granted ${{ review.hotel_amount }}
      toward your hotel stay.{% endif %}

You can test your template by sending yourself email messages.

The fields in the FinancialAidApplication and FinancialAidReviewData
records are subject to change, but you can review their current definitions
at https://github.com/caktus/pycon/blob/production/pycon/finaid/models.py


Templates
---------

Editing applications
~~~~~~~~~~~~~~~~~~~~

To create or edit an application, the app uses the ``finaid/edit.html``
template. The context provides a ``form`` variable containing the form.
A default template is provided that is customized to work with the PyCon
site and uses ``js/finaid.js`` to hide some of the fields unless some
other inputs have been checked, but the view doesn't care; it just wants
the form submitted.

Email notices
~~~~~~~~~~~~~

The text for many emails comes from templates whose paths start with "finaid".

Email template file names have this format:

finaid/{{ recipient }}/{{ event }}/[subject|body].txt

recipient can be:

* applicant
* reviewer

event can be:

* edited
* submitted
* message (a message was added to an application)

subject and body should be self-evident.

Subject templates should be a single line.

So for example, the templates used to notify a reviewer that the applicant
has edited their application are ``finaid/reviewer/edited/subject.txt``
and ``finaid/reviewer/edited/body.txt``.
