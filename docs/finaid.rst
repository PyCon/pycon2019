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
site and uses ``js/finaid.sh`` to hide some of the fields unless some
other inputs have been checked, but the view doesn't care; it just wants
the form submitted.
