"""
This is copied from the eldarion internal eldarion.test package.
"""

from __future__ import with_statement

from django.core.urlresolvers import reverse
from django.test import (TestCase as BaseTestCase,
    TransactionTestCase as BaseTransactionTestCase)


class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success,
            "login with username=%r, password=%r failed" % (user, password)
        )
    
    def __enter__(self):
        pass
    
    def __exit__(self, *args):
        self.testcase.client.logout()


class TestCaseMixin(object):
    def get(self, url_name, *args, **kwargs):
        return self.client.get(reverse(url_name, args=args, kwargs=kwargs))
    
    def post(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.client.post(reverse(url_name, args=args, kwargs=kwargs), data)
    
    def login(self, user, password):
        return login(self, user, password)
    
    def reload(self, obj):
        return obj.__class__._default_manager.get(pk=obj.pk)
    

class TestCase(BaseTestCase, TestCaseMixin):
    pass


class TransactionTestCase(BaseTransactionTestCase, TestCaseMixin):
    pass
