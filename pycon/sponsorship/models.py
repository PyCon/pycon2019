import datetime
from django.conf import settings

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import SET_NULL
from django.db.models.signals import post_init, post_save, pre_save
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.template import Context, Template

from django.contrib.auth.models import User
from multi_email_field.fields import MultiEmailField

from symposion.conference.models import Conference

from pycon.sponsorship import SPONSOR_COORDINATORS
from pycon.sponsorship.managers import SponsorManager
from symposion.utils.mail import send_email


# The benefits we track as individual fields on sponsors
# using separate SponsorBenefit records.
# Names are the names in the database as defined by PyCon organizers.
# Field names are the benefit names, lowercased, with
# spaces changed to _, and with "_benefit" appended.
# Column titles are arbitrary.

BENEFITS = [
    {
        'name': 'Print logo',
        'field_name': 'print_logo_benefit',
        'column_title': _(u'Print Logo'),
    },
    {
        'name': 'Advertisement',
        'field_name': 'advertisement_benefit',
        'column_title': _(u'Ad'),
    }
]


class SponsorLevel(models.Model):

    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
    available = models.BooleanField(default=True)
    display = models.BooleanField(default=True)
    order = models.IntegerField(_("order"), default=0)
    cost = models.PositiveIntegerField(_("cost"))
    description = models.TextField(_("description"), blank=True, help_text=_("This is private."))

    class Meta:
        ordering = ["conference", "order"]
        verbose_name = _("sponsor level")
        verbose_name_plural = _("sponsor levels")

    def __unicode__(self):
        return u"%s %s" % (self.conference, self.name)

    def sponsors(self):
        return self.sponsor_set.filter(active=True).order_by("added")


class SponsorPackage(models.Model):

    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
    available = models.BooleanField(default=True)
    display = models.BooleanField(default=True)
    order = models.IntegerField(_("order"), default=0)
    cost = models.PositiveIntegerField(_("cost"))
    description = models.TextField(_("description"), blank=True, help_text=_("This is private."))

    class Meta:
        ordering = ["conference", "order"]
        verbose_name = _("sponsor package")
        verbose_name_plural = _("sponsor packages")

    def __unicode__(self):
        return u"%s %s" % (self.conference, self.name)

    def sponsors(self):
        return self.sponsor_set.filter(active=True).order_by("added")


class Sponsor(models.Model):

    applicant = models.ForeignKey(User, related_name="sponsorships", verbose_name=_("applicant"), null=True, on_delete=SET_NULL)

    name = models.CharField(_("Sponsor Name"), max_length=100)
    display_url = models.CharField(
        _("Link text - text to display on link to sponsor webpage, if different from the actual link"),
        max_length=200,
        default='',
        blank=True
    )
    external_url = models.URLField(
        _("Link to sponsor webpage"),
        help_text=_("(Must include https:// or http://.)")
    )
    twitter_username = models.CharField(
        _("Twitter username"), blank=True, max_length=15,
    )
    annotation = models.TextField(_("annotation"), blank=True)
    contact_name = models.CharField(_("Contact Name"), max_length=100)
    contact_emails = MultiEmailField(
        _(u"Contact Emails"), default='',
        help_text=_(u"Please enter one email address per line.")
    )
    contact_phone = models.CharField(_(u"Contact Phone"), max_length=32)
    contact_address = models.TextField(_(u"Contact Address"))
    level = models.ForeignKey(SponsorLevel, verbose_name=_("level"))
    packages = models.ManyToManyField(SponsorPackage, verbose_name=_("packages"), blank=True)
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)

    active = models.BooleanField(_("active"), default=False)
    approval_time = models.DateTimeField(null=True, blank=True, editable=False)

    wants_table = models.BooleanField(
        _(
            'Does your organization want a table at the job fair? '
            '(See <a href="/2019/sponsors/fees/">Estimated Sponsor Fees</a> '
            'for costs that might be involved.)'
        ), default=False)
    wants_booth = models.BooleanField(
        _(
            'Does your organization want a booth on the expo floor? '
            '(See <a href="/2019/sponsors/fees/">Estimated Sponsor Fees</a> '
            'for costs that might be involved.)'
        ), default=False)
    small_entity_discount = models.BooleanField(
        _(
            'Does your organization have fewer than 25 employees,'
            ' which qualifies you for our Small Entity Discount of 30%?'
        ), default=False)

    # Whether things are complete
    # True = complete, False = incomplate, Null = n/a for this sponsor level
    print_logo_benefit = models.NullBooleanField(help_text=_(u"Print logo benefit is complete"))
    advertisement_benefit = models.NullBooleanField(help_text=_(u"Advertisement benefit is complete"))

    registration_promo_codes = models.CharField(max_length=200, blank=True, default='')
    expo_promo_codes = models.CharField(max_length=200, blank=True, default='')
    booth_number = models.IntegerField(blank=True, null=True, default=None)
    job_fair_participant = models.BooleanField(default=False)
    job_fair_table_number = models.IntegerField(blank=True, null=True, default=None)

    web_description = models.TextField(
        _(u"Company description (to show on the web site)"),
    )
    web_logo = models.ImageField(
        _(u"Web logo"),
        help_text=_("For display on our sponsor webpage. High resolution PNG or JPG, smallest dimension no less than 256px"),
        upload_to="sponsor_files",
        null=True,  # This is nullable in case old data doesn't have a web logo
        # We enforce it on all new or edited sponsors though.
    )
    print_logo = models.FileField(
        _(u"Print logo"),
        help_text=_("For printed materials, signage, and projection. SVG or EPS"),
        upload_to="sponsor_files",
        blank=True,
        null=True,  # This is nullable in case old data doesn't have a printed logo
        # We enforce it on all new or edited sponsors though.
    )

    objects = SponsorManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Set fields related to benefits being complete
        for benefit in BENEFITS:
            field_name = benefit['field_name']
            benefit_name = benefit['name']
            setattr(self, field_name, self.benefit_is_complete(benefit_name))
        super(Sponsor, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.active:
            return reverse("sponsor_detail", kwargs={"pk": self.pk})
        return reverse("sponsor_list")

    def get_display_url(self):
        """
        Return the text to display on the sponsor's link
        """
        if self.display_url:
            return self.display_url
        else:
            return self.external_url

    def render_email(self, text):
        """Replace special strings in text with values from the sponsor.

        %%NAME%% --> Sponsor name
        %%REGISTRATION_PROMO_CODES%% --> Registration promo codes, or empty string
        %%EXPO_PROMO_CODES%% --> Expo Hall only promo codes, or empty string
        %%BOOTH_NUMBER%% --> Booth number, or empty string if not set
        %%JOB_FAIR_TABLE_NUMBER%%" --> Job fair table number, or empty string if not set

        Flags:
          JOB_FAIR_PARTICIPANT: Use with {% if JOB_FAIR_PARTICIPANT %} block to
                                include some content for Job Fair Participants
        """
        text = text.replace("%%NAME%%", self.name)
        text = text.replace("%%REGISTRATION_PROMO_CODES%%",
                            self.registration_promo_codes or 'N/A')
        text = text.replace("%%EXPO_PROMO_CODES%%",
                            self.expo_promo_codes or 'N/A')

        # The next two are numbers, or if not set, None.  We don't want to
        # display "None" :-), but we might want to display "0".
        booth = str(self.booth_number) if self.booth_number is not None else ""
        text = text.replace("%%BOOTH_NUMBER%%", booth)
        table = str(self.job_fair_table_number) if self.job_fair_table_number is not None else ""
        text = text.replace("%%JOB_FAIR_TABLE_NUMBER%%", table)
        email_template = Template(text)
        email_context = Context({
            'JOB_FAIR_PARTICIPANT': self.job_fair_participant,
        })
        text = email_template.render(email_context)
        return text

    @cached_property
    def website_logo_url(self):
        if self.web_logo:
            return self.web_logo.url

    @property
    def joblisting_text(self):
        if not hasattr(self, "_joblisting_text"):
            self._joblisting_text = None
            benefits = self.sponsor_benefits.filter(
                benefit__name__startswith='Job Listing',
            )
            if benefits.count():
                self._joblisting_text = benefits[0].text
        return self._joblisting_text

    @property
    def website_logo(self):
        return self.web_logo

    def reset_benefits(self):
        """
        Reset all benefits for this sponsor to the defaults for their
        sponsorship level.
        """
        level = None

        try:
            level = self.level
        except SponsorLevel.DoesNotExist:
            pass

        try:
            packages = self.packages
        except SponsorPackage.DoesNotExist:
            pass

        allowed_benefits = []
        if level:
            for benefit_level in level.benefit_levels.all():
                # Create all needed benefits if they don't exist already
                sponsor_benefit, created = SponsorBenefit.objects.get_or_create(
                    sponsor=self, benefit=benefit_level.benefit)

                # and set to default limits for this level.
                sponsor_benefit.max_words = benefit_level.max_words
                sponsor_benefit.other_limits = benefit_level.other_limits

                # and set to active
                sponsor_benefit.active = True

                # @@@ We don't call sponsor_benefit.clean here. This means
                # that if the sponsorship level for a sponsor is adjusted
                # downwards, an existing too-long text entry can remain,
                # and won't raise a validation error until it's next
                # edited.
                sponsor_benefit.save()

                allowed_benefits.append(sponsor_benefit.pk)

        if packages:
            for package in packages.all():
                for benefit_package in package.benefit_packages.all():
                    # Create all needed benefits if they don't exist already
                    sponsor_benefit, created = SponsorBenefit.objects.get_or_create(
                        sponsor=self, benefit=benefit_package.benefit)

                    # and set to default limits for this level.
                    sponsor_benefit.max_words = benefit_package.max_words
                    sponsor_benefit.other_limits = benefit_package.other_limits

                    # and set to active
                    sponsor_benefit.active = True

                    # @@@ We don't call sponsor_benefit.clean here. This means
                    # that if the sponsorship level for a sponsor is adjusted
                    # downwards, an existing too-long text entry can remain,
                    # and won't raise a validation error until it's next
                    # edited.
                    sponsor_benefit.save()

                    allowed_benefits.append(sponsor_benefit.pk)

        # Any remaining sponsor benefits that don't normally belong to
        # this level are set to inactive
        self.sponsor_benefits.exclude(pk__in=allowed_benefits).update(active=False, max_words=None, other_limits="")

    # @@@ should this just be done centrally?
    def send_coordinator_emails(self):
        for user in User.objects.filter(groups__name=SPONSOR_COORDINATORS):
            send_email(
                [user.email], "sponsor_signup",
                context={"sponsor": self}
            )

    def benefit_is_complete(self, name):
        """Return True - benefit is complete, False - benefit is not complete,
         or None - benefit not applicable for this sponsor's level """
        if BenefitLevel.objects.filter(level=self.level, benefit__name=name).exists():
            try:
                benefit = self.sponsor_benefits.get(benefit__name=name)
            except SponsorBenefit.DoesNotExist:
                return False
            else:
                return benefit.is_complete
        else:
            return None   # Not an applicable benefit for this sponsor's level


def _store_initial_level(sender, instance, **kwargs):
    if instance:
        instance._initial_level_id = instance.level_id
        try:
            instance._initial_packages = instance.packages.all()
        except ValueError:
            instance._initial_packages = []
post_init.connect(_store_initial_level, sender=Sponsor)


def _check_level_change(sender, instance, created, **kwargs):
    if instance and (created or instance.level_id != instance._initial_level_id or instance.packages.all() != instance._initial_packages):
        instance.reset_benefits()
post_save.connect(_check_level_change, sender=Sponsor)


def _send_confirmation(sender, instance, created, **kwargs):
    """
    Send an email to the sponsors mailing list when a new application is
    submitted.
    """
    if created:
        send_email(
            to=[settings.SPONSORSHIP_EMAIL],
            kind='new_sponsor',
            context={
                'sponsor': instance,
            },
        )
        send_email(
            to=instance.contact_emails,
            kind='new_sponsor_confirm',
            context={'sponsor': instance}
        )
post_save.connect(_send_confirmation, sender=Sponsor)


def _store_initial_active(sender, instance, **kwargs):
    if instance:
        instance._initial_active = instance.active
post_init.connect(_store_initial_active, sender=Sponsor)
post_save.connect(_store_initial_active, sender=Sponsor)


def _check_active_change(sender, instance, **kwargs):
    if instance:
        if instance.active:
            if not instance._initial_active or not instance.approval_time:
                # Instance is newly active.
                instance.approval_time = datetime.datetime.now()
        else:
            instance.approval_time = None
pre_save.connect(_check_active_change, sender=Sponsor)


def _send_sponsor_notification_emails(sender, instance, created, **kwargs):
    if instance and created:
        instance.send_coordinator_emails()
post_save.connect(_send_sponsor_notification_emails, sender=Sponsor)


class Benefit(models.Model):

    name = models.CharField(_("name"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)
    type = models.CharField(
        _("type"),
        choices=[
            ("text", "Text"),
            ("richtext", "Rich Text"),
            ("file", "File"),
            ("weblogo", "Web Logo"),
            ("simple", "Simple")
        ],
        max_length=10,
        default="simple"
    )

    def __unicode__(self):
        return self.name


class BenefitLevel(models.Model):

    benefit = models.ForeignKey(
        Benefit,
        related_name="benefit_levels",
        verbose_name=_("benefit")
    )
    level = models.ForeignKey(
        SponsorLevel,
        related_name="benefit_levels",
        verbose_name=_("level")
    )
    max_words = models.PositiveIntegerField(_("max words"), blank=True, null=True)
    other_limits = models.CharField(_("other limits"), max_length=200, blank=True)

    class Meta:
        ordering = ["level"]

    def __unicode__(self):
        return u"%s - %s" % (self.level, self.benefit)


class BenefitPackage(models.Model):

    benefit = models.ForeignKey(
        Benefit,
        related_name="benefit_packages",
        verbose_name=_("benefit")
    )
    package = models.ForeignKey(
        SponsorPackage,
        related_name="benefit_packages",
        verbose_name=_("package")
    )
    max_words = models.PositiveIntegerField(_("max words"), blank=True, null=True)
    other_limits = models.CharField(_("other limits"), max_length=200, blank=True)

    class Meta:
        ordering = ["package"]

    def __unicode__(self):
        return u"%s - %s" % (self.package, self.benefit)


class SponsorBenefit(models.Model):

    sponsor = models.ForeignKey(
        Sponsor,
        related_name="sponsor_benefits",
        verbose_name=_("sponsor")
    )
    benefit = models.ForeignKey(
        Benefit,
        related_name="sponsor_benefits",
        verbose_name=_("benefit")
    )
    active = models.BooleanField(default=True)

    # Limits: will initially be set to defaults from corresponding BenefitLevel
    max_words = models.PositiveIntegerField(_("max words"), blank=True, null=True)
    other_limits = models.CharField(_("other limits"), max_length=200, blank=True)

    # Data: zero or one of these fields will be used, depending on the
    # type of the Benefit (text, file, or simple)
    text = models.TextField(_("text"), blank=True)
    upload = models.FileField(_("file"), blank=True, upload_to="sponsor_files")

    # Whether any assets required from the sponsor have been provided
    # (e.g. a logo file for a Web logo benefit).
    is_complete = models.NullBooleanField(help_text=_(u"True - benefit complete; False - benefit incomplete; Null - n/a"))

    class Meta:
        ordering = ['-active']

    def __unicode__(self):
        return u"%s - %s (%s)" % (self.sponsor, self.benefit,
                                  self.benefit.type)

    def save(self, *args, **kwargs):
        # Validate - save() doesn't clean your model by default, so call
        # it explicitly before saving
        self.full_clean()
        self.is_complete = self._is_complete()
        super(SponsorBenefit, self).save(*args, **kwargs)

    def clean(self):
        if self.max_words and len(self.text.split()) > self.max_words:
            raise ValidationError("Sponsorship level only allows for %s "
                                  "words." % self.max_words)
        editable_fields = self.data_fields()
        if bool(self.text) and 'text' not in editable_fields:
            raise ValidationError("Benefit type %s may not have text"
                                  % self.benefit.type)
        if bool(self.upload) and 'upload' not in editable_fields:
            raise ValidationError("Benefit type %s may not have an uploaded "
                                  "file (%s)" % (self.benefit.type,
                                                 self.upload))

    def data_fields(self):
        """
        Return list of data field names which should be editable for
        this ``SponsorBenefit``, depending on its ``Benefit`` type.
        """
        if self.benefit.type == "file" or self.benefit.type == "weblogo":
            return ["upload"]
        elif self.benefit.type in ("text", "richtext", "simple"):
            return ["text"]
        return []

    def _is_complete(self):
        return self.active and \
            ((self.benefit.type in ('text', 'richtext') and bool(self.text))
                or (self.benefit.type in ('file', 'weblogo') and bool(self.upload)))
