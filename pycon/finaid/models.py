from decimal import Decimal
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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
STATUS_NEED_MORE = 8

STATUS_CHOICES = (
    (STATUS_SUBMITTED, _(u"Submitted")),
    (STATUS_WITHDRAWN, _(u"Withdrawn")),
    (STATUS_INFO_NEEDED, _(u"Information needed")),
    (STATUS_OFFERED, _(u"Offered")),
    (STATUS_NEED_MORE, _(u"Requesting more funds")),
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
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    last_update = models.DateTimeField(auto_now=True, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='financial_aid', db_index=True)

    pyladies_grant_requested = models.BooleanField(
        verbose_name=_("PyLadies grant"),
        help_text=_("Would you like to be considered for a "
                    "PyLadies grant? (Women only.)"))

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
        help_text=_("Please describe your travel plans"))

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
    portfolios = models.CharField(
        verbose_name=_("Portfolios"),
        help_text=_("Please provide links to any portfolios you have "
                    "that contain Python work. (e.g. Github, "
                    "Bitbucket, etc.)"),
        max_length=500, blank=True)
    use_of_python = models.CharField(
        verbose_name=_("Use of Python"),
        help_text=_("Describe your use of Python"), max_length=500)
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

    def get_last_update(self):
        """Return last time the application or its review data or
        its attached messages were updated"""
        last_update = self.last_update
        try:
            last_review_update = self.review.last_update
        except FinancialAidReviewData.DoesNotExist:
            pass
        else:
            last_update = max(last_update, last_review_update)
        for msg in self.messages.all():
            last_update = max(last_update, msg.submitted_at)
        return last_update

    def get_last_update_display(self):
        return unicode(self.get_last_update())

    def fa_app_url(self):
        """URL for the detail view of a financial aid application"""
        return reverse('finaid_review_detail', args=[str(self.pk)])


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
    last_update = models.DateTimeField(auto_now=True,
                                       editable=False)
    status = models.IntegerField(choices=STATUS_CHOICES,
                                 default=STATUS_SUBMITTED)
    travel_amount = models.DecimalField(
        decimal_places=2, max_digits=8, default=Decimal("0.00"))
    grant_letter_sent = models.DateField(blank=True, null=True)
    cash_check = models.IntegerField(choices=PAYMENT_CHOICES,
                                     blank=True, null=True)
    notes = models.TextField(blank=True)
    travel_cash_check = models.IntegerField(choices=PAYMENT_CHOICES,
                                            blank=True, null=True)
    disbursement_notes = models.TextField(blank=True)
    promo_code = models.CharField(blank=True, max_length=20)


class FinancialAidEmailTemplate(models.Model):
    """Template for bulk mailing applicants"""
    name = models.CharField(max_length=80)
    template = models.TextField(
        help_text=u"Django template used to compose text email to applicants."
                  u"Context variables include 'application' and 'review'"
    )

    def __unicode__(self):
        return self.name
