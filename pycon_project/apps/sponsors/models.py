import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


class SponsorLevel(models.Model):
    
    name = models.CharField(_("name"), max_length=100)
    order = models.IntegerField(_("order"), default=0)
    description = models.TextField(_("description"), blank=True, help_text=_("This is private."))
    
    class Meta:
        ordering = ["order"]
    
    def __unicode__(self):
        return self.name


class Sponsor(models.Model):
    
    applicant = models.OneToOneField(
        User, related_name="sponsorship", verbose_name=_("applicant")
    )
    name = models.CharField(_("name"), max_length=100)
    external_url = models.URLField(_("external URL"))
    annotation = models.TextField(_("annotation"), blank=True)
    contact_name = models.CharField(_("contact name"), max_length=100)
    contact_email = models.EmailField(_(u"Contact e\u2011mail"))
    level = models.ForeignKey(SponsorLevel, verbose_name=_("level"), null=True)
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)
    active = models.NullBooleanField(_("active"), choices=[
        (True, "approved"),
        (False, "rejected"),
        (None, "unreviewed"),
    ])
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        if self.active:
            return reverse("sponsor_detail", kwargs={"pk": self.pk})
        return reverse("sponsor_index")
    
    @property
    def website_logo_url(self):
        try:
            logo = SponsorLogo.objects.get(sponsor=self, label="website")
        except SponsorLogo.DoesNotExist:
            return u""
        else:
            return logo.logo.url


class SponsorLogo(models.Model):
    
    sponsor = models.ForeignKey(Sponsor, verbose_name=_("sponsor"))
    label = models.CharField(
        max_length = 100,
        help_text = _("To display this logo on site use label 'website'")
    )
    logo = models.ImageField(_("logo"), upload_to="sponsor_logos/")
    
    class Meta:
        unique_together = [("sponsor", "label")]
