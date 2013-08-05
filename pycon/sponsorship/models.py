import datetime

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_init, post_save
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from symposion.conference.models import Conference

from pycon.sponsorship import SPONSOR_COORDINATORS
from pycon.sponsorship.managers import SponsorManager
# from symposion.utils.mail import send_email


class SponsorLevel(models.Model):
    
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
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


class Sponsor(models.Model):
    
    applicant = models.ForeignKey(User, related_name="sponsorships", verbose_name=_("applicant"), null=True)
    
    name = models.CharField(_("Sponsor Name"), max_length=100)
    display_url = models.URLField(_("display URL"), blank=True)
    external_url = models.URLField(_("external URL"))
    annotation = models.TextField(_("annotation"), blank=True)
    contact_name = models.CharField(_("Contact Name"), max_length=100)
    contact_email = models.EmailField(_(u"Contact Email"))
    level = models.ForeignKey(SponsorLevel, verbose_name=_("level"))
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)
    active = models.BooleanField(_("active"), default=False)

    # Denormalization (this assumes only one logo)
    sponsor_logo = models.ForeignKey("SponsorBenefit", related_name="+", null=True, blank=True, editable=False)

    objects = SponsorManager()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")
    
    def get_absolute_url(self):
        if self.active:
            return reverse("sponsor_detail", kwargs={"pk": self.pk})
        return reverse("sponsor_list")
    
    def get_display_url(self):
        if self.display_url:
            return self.display_url
        else:
            return self.external_url

    @property
    def website_logo_url(self):
        if not hasattr(self, "_website_logo_url"):
            self._website_logo_url = None
            benefits = self.sponsor_benefits.filter(benefit__type="weblogo", upload__isnull=False)
            if benefits.exists():
                # @@@ smarter handling of multiple weblogo benefits?
                # shouldn't happen
                if benefits[0].upload:
                    self._website_logo_url = benefits[0].upload.url
        return self._website_logo_url
    
    @property
    def listing_text(self):
        if not hasattr(self, "_listing_text"):
            self._listing_text = None
            benefits = self.sponsor_benefits.filter(benefit__id=7)
            if benefits.count():
                self._listing_text = benefits[0].text
        return self._listing_text
    
    @property
    def joblisting_text(self):
        if not hasattr(self, "_joblisting_text"):
            self._joblisting_text = None
            benefits = self.sponsor_benefits.filter(benefit__id=8)
            if benefits.count():
                self._joblisting_text = benefits[0].text
        return self._joblisting_text
    
    @property
    def website_logo(self):
        if self.sponsor_logo is None:
            benefits = self.sponsor_benefits.filter(benefit__type="weblogo", upload__isnull=False)[:1]
            if benefits.count():
                if benefits[0].upload:
                    self.sponsor_logo = benefits[0]
                    self.save()
        return self.sponsor_logo.upload
    
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
        
        # Any remaining sponsor benefits that don't normally belong to
        # this level are set to inactive
        self.sponsor_benefits.exclude(pk__in=allowed_benefits).update(active=False, max_words=None, other_limits="")
    
    # @@@ should this just be done centrally?
    def send_coordinator_emails(self):
        for user in User.objects.filter(groups__name=SPONSOR_COORDINATORS):
            send_email(
                [user.email], "sponsor_signup",
                context = {"sponsor": self}
            )


def _store_initial_level(sender, instance, **kwargs):
    if instance:
        instance._initial_level_id = instance.level_id
post_init.connect(_store_initial_level, sender=Sponsor)


def _check_level_change(sender, instance, created, **kwargs):
    if instance and (created or instance.level_id != instance._initial_level_id):
        instance.reset_benefits()
post_save.connect(_check_level_change, sender=Sponsor)


def _send_sponsor_notification_emails(sender, instance, created, **kwargs):
    if instance and created:
        instance.send_coordinator_emails()
post_save.connect(_send_sponsor_notification_emails, sender=Sponsor)


class Benefit(models.Model):
    
    name = models.CharField(_("name"), max_length=100)
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


class SponsorBenefit(models.Model):
    
    sponsor = models.ForeignKey(
        Sponsor,
        related_name="sponsor_benefits",
        verbose_name=_("sponsor")
    )
    benefit = models.ForeignKey(Benefit,
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
    
    class Meta:
        ordering = ['-active']
    
    def __unicode__(self):
        return u"%s - %s (%s)" % (self.sponsor, self.benefit,
                                  self.benefit.type)

    def save(self, *args, **kwargs):
        # Validate - save() doesn't clean your model by default, so call
        # it explicitly before saving
        self.full_clean()
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


def _denorm_weblogo(sender, instance, created, **kwargs):
    if instance:
        if instance.benefit.type == "weblogo" and instance.upload:
            sponsor = instance.sponsor
            sponsor.sponsor_logo = instance
            sponsor.save()
post_save.connect(_denorm_weblogo, sender=SponsorBenefit)
