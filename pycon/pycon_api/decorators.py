from __future__ import unicode_literals
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, Http404
from functools import update_wrapper
from pycon.pycon_api.exceptions import AuthenticationError
from pycon.pycon_api.models import APIAuth
import json


# We need to be able to serialize a datetime object, which the built-in
# encoder won't do. We also want to be sure to use a known format that
# preserved microseconds.
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
class JSONDatetimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime(DATETIME_FORMAT)
        else:
            return super(JSONDatetimeEncoder, self).default(o)


def api_view(method):
    """Decorator that forces the view to require a valid
    API key in order to be processed.

    Calls to the view that do not have an appropriate key
    will return a 401 response.
    """
    def f(request, *args, **kwargs):
        # Ensure that there is an appropriate key attached
        # to this request, and return a 401 otherwise.
        try:
            APIAuth.verify_request(request)
        except AuthenticationError as ex:
            return HttpResponse(
                content=json.dumps({
                    'code': 403,
                    'error': unicode(ex).strip("'"),
                }),
                content_type='application/json',
                status=403,
            )

        # Run the decorated method.
        try:
            response = method(request, *args, **kwargs)
            code = 200

            # Sanity check: Did we get a tuple back?
            # This shorthand provides me an easy way to send back
            # a success response that is not a 200.
            if isinstance(response, tuple) and len(response) == 2:
                response, code = response

            return HttpResponse(
                json.dumps({
                    'code': code,
                    'data': response,
                }, cls=JSONDatetimeEncoder),
                content_type='application/json',
                status=code,
            )
        except Http404 as ex:
            msg = unicode(ex).strip("'")
            return HttpResponse(
                content=json.dumps({
                    'code': 404,
                    'error': msg if msg else 'not found',    
                }),
                content_type='application/json',
                status=404,
            )
            
    return update_wrapper(f, method)
