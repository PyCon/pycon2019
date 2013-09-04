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
