Deploying
=========

Some notes on deploying.

Periodic tasks
--------------

Arrange to run this command every day or so to expunge the data from
deleted accounts if more than 48 hours since they were deleted::

    python manage.py expunge_deleted
    
