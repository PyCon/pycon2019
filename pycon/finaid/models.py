from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


SEX_CHOICES = (
    (0, '-'),
    (1, _('Female')),
    (2, _('Male')),
)

PRESENTING_CHOICES = (
    (1, _("Yes")),
    (2, _("No")),
    (3, _("I have applied but don't know yet")),
)

STATUS_SUBMITTED = 1
STATUS_WITHDRAWN = 2
STATUS_INFO_NEEDED = 3
STATUS_OFFERED = 4
STATUS_REJECTED = 5
STATUS_DECLINED = 6
STATUS_ACCEPTED = 7

STATUS_CHOICES = (
    (STATUS_SUBMITTED, _(u"Submitted")),
    (STATUS_WITHDRAWN, _(u"Withdrawn")),
    (STATUS_INFO_NEEDED, _(u"Information needed")),
    (STATUS_OFFERED, _(u"Offered")),
    (STATUS_REJECTED, _(u"Rejected")),
    (STATUS_DECLINED, _(u"Declined")),
    (STATUS_ACCEPTED, _(u"Accepted"))
)


class FinancialAidApplication(models.Model):
    # The primary key ('id') is used as application number
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='financial_aid', db_index=True)

    status = models.IntegerField(choices=STATUS_CHOICES,
                                 default=STATUS_SUBMITTED)

    pyladies_grant_requested = models.BooleanField(help_text=_("Would you like to be considered for a PyLadies grant?"))
    registration_grant_requested = models.BooleanField(help_text=_("Will you need assistance with the Conference Registration?"))

    hotel_grant_requested = models.BooleanField(help_text=_("Will you need assistance with a Hotel Room?"))
    hotel_nights = models.IntegerField(help_text=_("How many nights will you be staying at the hotel?"), default=0)
    sex = models.IntegerField(choices=SEX_CHOICES,
                              help_text=_("(Your sex is used only to help assign roommates for those requesting hotel assistance)"),
                              default=0,   # e.g. "-" meaning no answer,
                              blank=True,  # So the form won't show this field as required
                              )

    travel_grant_requested = models.BooleanField(help_text=_("Will you need assistance with Travel Costs?"))
    international = models.BooleanField(help_text=_("Will you be traveling internationally?"))
    travel_amount_requested = models.DecimalField(help_text=_("Please enter the amount of travel assistance you need, in US dollars."), decimal_places=2, max_digits=8, default=Decimal("0.00"))
    travel_plans = models.CharField(max_length=1024, help_text=_("Please describe your travel plans"), blank=True)

    tutorial_grant_requested = models.BooleanField(help_text=_("Will you need assistance with tutorials?"))

    profession = models.CharField(help_text=_("What is it that you do"), max_length=500)
    involvement = models.CharField(help_text=_("Describe your involvement in any open source projects or community."), blank=True, max_length=1024)
    what_you_want = models.CharField(help_text=_("What do you want to get out of attending PyCon?"), max_length=500)
    want_to_learn = models.CharField(help_text=_("What is it that you're hoping to learn?"), max_length=500)
    portfolios = models.CharField(help_text=_("Please provide links to any portfolios you have that contain Python work. (e.g. Github, Bitbucket, etc.)"), max_length=500, blank=True)
    use_of_python = models.CharField(help_text=_("Describe your use of Python"), max_length=500)
    beginner_resources = models.CharField(help_text=_("If you're a beginner, describe the resources you're using to learn Python."), max_length=500, blank=True)
    presenting = models.IntegerField(help_text=_("Will you be speaking, hosting a poster session, or otherwise presenting at PyCon?"), choices=PRESENTING_CHOICES)
    experience_level = models.CharField(help_text=_("What is your experience level with Python?"), max_length=200)
    presented = models.BooleanField(help_text=_("Have you spoken at PyCon in the past?"))
    first_time = models.BooleanField(help_text=_("Is this your first time attending PyCon?"))

    def __unicode__(self):
        return u"Financial aid application for %s" % self.user
