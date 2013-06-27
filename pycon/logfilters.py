import logging


class QuotelessStr(str):
    """
    Return the repr() of this string *without* quotes.  This is a
    temporary fix until https://github.com/severb/graypy/pull/34 is resolved.
    """
    def __repr__(self):
        return self


class StaticFieldFilter(logging.Filter):
    """
    Python logging filter that adds the given static contextual information
    in the ``fields`` dictionary to all logging records.
    """
    def __init__(self, fields):
        self.static_fields = fields

    def filter(self, record):
        for k, v in self.static_fields.items():
            setattr(record, k, QuotelessStr(v))
        return True


class RequestFilter(logging.Filter):
    """
    Python logging filter that removes the (non-pickable) Django ``request``
    object from the logging record.
    """
    def filter(self, record):
        if hasattr(record, 'request'):
            del record.request
        return True
