import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from symposion.proposals.models import ProposalBase


class APIAuth(models.Model):
    """API Users need to have a record in this table"""
    name = models.CharField(max_length=100,
                            help_text=_("Name or other description of user"))
    auth_key = models.CharField(default=lambda: str(uuid.uuid4()),
                                max_length=36)
    enabled = models.BooleanField(default=True)

    @classmethod
    def check_key(cls, auth_key):
        """Return true if the auth_key is valid"""
        return cls.objects.filter(enabled=True, auth_key=auth_key).exists()


class ProposalData(models.Model):
    """A chunk of text data associated with a proposal"""
    # Probably JSON, but doesn't have to be
    proposal = models.OneToOneField(ProposalBase, db_index=True,
                                    related_name='data')
    data = models.TextField()


class IRCLogLine(models.Model):
    timestamp = models.DateTimeField()
    proposal = models.ForeignKey(ProposalBase)
    user = models.CharField(max_length=40)
    line = models.TextField(blank=True)

