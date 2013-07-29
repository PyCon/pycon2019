from decimal import Decimal
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


SEX_NO_ANSWER = 0
SEX_CHOICES = (
    (SEX_NO_ANSWER, '-'),
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

PAYMENT_CASH = 1
PAYMENT_CHECK = 2
PAYMENT_CHOICES = (
    (PAYMENT_CASH, _(u"Cash")),
    (PAYMENT_CHECK, _(u"Check")),
)


class FinancialAidApplication(models.Model):
    # The primary key ('id') is used as application number
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='financial_aid', db_index=True)

    pyladies_grant_requested = models.BooleanField(
        verbose_name=_("PyLadies grant"),
        help_text=_("Would you like to be considered for a "
                    "PyLadies grant?"))
    registration_grant_requested = models.BooleanField(
        verbose_name=_("Registration grant"),
        help_text=_("Will you need assistance with the "
                    "Conference Registration?"))

    hotel_grant_requested = models.BooleanField(
        verbose_name=_("Hotel grant"),
        help_text=_("Will you need assistance with a Hotel Room?"))
    hotel_nights = models.IntegerField(
        verbose_name=_("Nights"),
        help_text=_("How many nights will you be staying at the hotel?"),
        default=0)
    hotel_arrival_date = models.DateField(
        verbose_name=_(u"Hotel arrival date"),
        help_text=u"YYYY-MM-DD",  # Ugh - this should really be on the widget
        default=datetime.date.today,
    )
    hotel_departure_date = models.DateField(
        verbose_name=_(u"Hotel departure date"),
        help_text=u"YYYY-MM-DD",  # Ugh - this should really be on the widget
        default=datetime.date.today,
    )
    sex = models.IntegerField(
        verbose_name=_("Sex"),
        choices=SEX_CHOICES,
        help_text=_("(Your sex will be used only to help assign roommates "
                    "for those requesting hotel assistance)"),
        default=SEX_NO_ANSWER,
        blank=True,  # So the form won't show this field as required
    )

    travel_grant_requested = models.BooleanField(
        verbose_name=_("Travel grant"),
        help_text=_("Will you need assistance with Travel Costs?"))
    international = models.BooleanField(
        verbose_name=_("International"),
        help_text=_("Will you be traveling internationally?"))
    travel_amount_requested = models.DecimalField(
        verbose_name=_("Travel amount"),
        help_text=_("Please enter the amount of travel assistance you "
                    "need, in US dollars."),
        decimal_places=2, max_digits=8, default=Decimal("0.00"))
    travel_plans = models.CharField(
        verbose_name=_("Travel plans"),
        max_length=1024,
        help_text=_("Please describe your travel plans"), blank=True)

    tutorial_grant_requested = models.BooleanField(
        verbose_name=_("Tutorial grant"),
        help_text=_("Will you need assistance with tutorials?"))

    profession = models.CharField(
        verbose_name=_("Profession"),
        help_text=_("What is it that you do"), max_length=500)
    involvement = models.CharField(
        verbose_name=_("Involvement"),
        help_text=_("Describe your involvement in any open source "
                    "projects or community."),
        blank=True, max_length=1024)
    what_you_want = models.CharField(
        verbose_name=u"What you want",
        help_text=_("What do you want to get out of attending PyCon?"),
        max_length=500)
    want_to_learn = models.CharField(
        verbose_name=u"Want to learn",
        help_text=_("What is it that you're hoping to learn?"),
        max_length=500)
    portfolios = models.CharField(
        verbose_name=_("Portfolios"),
        help_text=_("Please provide links to any portfolios you have "
                    "that contain Python work. (e.g. Github, "
                    "Bitbucket, etc.)"),
        max_length=500, blank=True)
    use_of_python = models.CharField(
        verbose_name=_("Use of Python"),
        help_text=_("Describe your use of Python"), max_length=500)
    beginner_resources = models.CharField(
        verbose_name=_("Beginner resources"),
        help_text=_("If you're a beginner, describe the resources you're "
                    "using to learn Python."),
        max_length=500, blank=True)
    presenting = models.IntegerField(
        verbose_name=_("Presenting"),
        help_text=_("Will you be speaking, hosting a poster session, "
                    "or otherwise presenting at PyCon?"),
        choices=PRESENTING_CHOICES)
    experience_level = models.CharField(
        verbose_name=_("Python experience level"),
        help_text=_("What is your experience level with Python?"),
        max_length=200)
    first_time = models.BooleanField(
        verbose_name=_("First time"),
        help_text=_("Is this your first time attending PyCon?"))
    presented = models.BooleanField(
        verbose_name=_("Presented"),
        help_text=_("Have you spoken at PyCon in the past?"),
        default=False)

    def __unicode__(self):
        return u"Financial aid application for %s" % self.user

    @property
    def status(self):
        try:
            return self.review.status
        except FinancialAidReviewData.DoesNotExist:
            return STATUS_SUBMITTED  # Default status

    def get_status_display(self):
        try:
            return self.review.get_status_display()
        except FinancialAidReviewData.DoesNotExist:
            return _(u"Submitted")


class FinancialAidMessage(models.Model):
    """Message attached to a financial aid application."""
    application = models.ForeignKey(FinancialAidApplication,
                                    related_name="messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             help_text=_(u"User who submitted the message"))
    visible = models.BooleanField(
        default=False,
        help_text=_(u"Whether message is visible to applicant"))
    message = models.TextField()
    submitted_at = models.DateTimeField(default=datetime.datetime.now,
                                        editable=False)

    class Meta:
        ordering = ["submitted_at"]

    def __unicode__(self):
        return u"Financial aid application message for %s" \
               % self.application.user

    def has_seen(self, user):
        """Return True if this user has seen this message"""
        return self.seen.filter(user=user).exists()

    @classmethod
    def unseen(cls, user):
        """
        Return queryset of all messages, on any application and by any
        user, this user has not seen.
        Typically you'd filter this further on a particular application
        or something."""
        return cls.objects.exclude(seen__user=user)


class FinancialAidApplicationPeriod(models.Model):
    """Represents periods when applications are open"""
    start = models.DateTimeField()
    end = models.DateTimeField()

    @classmethod
    def open(cls):
        """Return True if applications are open right now"""
        now = datetime.datetime.now()
        return bool(cls._default_manager.filter(start__lt=now, end__gt=now))

    def __unicode__(self):
        return u"Applications open %s-%s" % (self.start, self.end)


class FinancialAidReviewData(models.Model):
    """
    Data used by reviewers - about amounts granted, delivery of
    funds, etc etc.
    """
    application = models.OneToOneField(FinancialAidApplication,
                                       related_name='review',
                                       editable=False)
    status = models.IntegerField(choices=STATUS_CHOICES,
                                 default=STATUS_SUBMITTED)
    hotel_amount = models.DecimalField(
        decimal_places=2, max_digits=8, default=Decimal("0.00"))
    paired_with = models.ForeignKey(User, blank=True, null=True)
    hotel_notes = models.TextField(blank=True)
    travel_amount = models.DecimalField(
        decimal_places=2, max_digits=8, default=Decimal("0.00"))
    tutorial_amount = models.DecimalField(
        decimal_places=2, max_digits=8, default=Decimal("0.00"))
    registration_amount = models.DecimalField(
        decimal_places=2, max_digits=8, default=Decimal("0.00"))
    # sum is not a field in the model; we compute it at display time
    grant_letter_sent = models.DateField(blank=True, null=True)
    cash_check = models.IntegerField(choices=PAYMENT_CHOICES,
                                     blank=True, null=True)
    notes = models.TextField(blank=True)
    travel_signed = models.BooleanField(blank=True)
    travel_cash_check = models.IntegerField(choices=PAYMENT_CHOICES,
                                            blank=True, null=True)
    travel_check_number = models.CharField(max_length=10, blank=True)
    travel_preferred_disbursement = models.TextField(blank=True)
    promo_code = models.CharField(blank=True, max_length=20)

    def sum(self):
        """Sum of amounts granted"""
        return self.hotel_amount + self.travel_amount \
            + self.tutorial_amount + self.registration_amount
