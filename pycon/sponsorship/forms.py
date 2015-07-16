from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.core.exceptions import ValidationError
from django.forms import formset_factory, Form
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from djangoformsetjs.utils import formset_media_js

from pycon.sponsorship.models import Sponsor, SponsorBenefit


class ContactEmailForm(Form):
    # This could be a ModelForm, but after several wasted hours, I gave up on
    # trying to get model formsets working.  Plain old forms seem simpler in
    # this case, anyway.
    email = forms.EmailField()


BaseContactEmailFormSet = formset_factory(
    form=ContactEmailForm,
    can_delete=True,
    extra=0,
    # We don't set min_num and validate_min here because it results in an
    # unhelpful "Please submit at least N forms" message. We check ourselves
    # in a custom clean method instead, so we can say "Please provide at
    # least one email address" and also check for blank addresses etc.
)


class ContactEmailFormSet(BaseContactEmailFormSet):
    def save(self, sponsor):
        """
        Add or remove contact emails to match up to the list in this formset.
        This is something that a model formset would do for us, if we'd been
        able to get them to work here. Ah well.
        """
        emails = self.get_emails()
        sponsor_emails = sponsor.contact_emails.all().values_list('email', flat=True)
        # Remove any that have been deleted
        for email in sponsor_emails:
            if email not in emails:
                sponsor.contact_emails.filter(email=email).delete()
        # Add any not already in the list
        for email in emails:
            if email not in sponsor_emails:
                sponsor.contact_emails.create(email=email)

    @cached_property
    def undeleted_forms(self):
        deleted_forms = self.deleted_forms
        return [form for form in self.forms if form not in deleted_forms]

    def get_emails(self):
        return [email
                for email in [form.cleaned_data.get('email', False)
                              for form in self.undeleted_forms]
                if email]

    def clean(self):
        emails = self.get_emails()
        if not emails:
            raise ValidationError(_("At least one email address is required"))
        if len(emails) != len(set([email.lower() for email in emails])):
            raise ValidationError(_("Emails must be unique, regardless of case"))



class SponsorApplicationForm(forms.ModelForm):
    class Media(object):
        js = formset_media_js

    class Meta:
        model = Sponsor
        fields = ["name", "contact_name", "contact_phone",
                  "contact_address",
                  "external_url",
                  "level", "wants_table", "wants_booth"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        kwargs.update({
            "initial": {
                "contact_name": self.user.get_full_name(),
            }
        })
        super(SponsorApplicationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(SponsorApplicationForm, self).save(commit=False)
        obj.applicant = self.user
        if commit:
            obj.save()
        return obj


class SponsorDetailsForm(forms.ModelForm):
    class Media(object):
        js = formset_media_js

    class Meta:
        model = Sponsor
        fields = [
            "name",
            "external_url",
            "contact_name",
        ]


class SponsorBenefitsInlineFormSet(BaseInlineFormSet):

    def _construct_form(self, i, **kwargs):
        form = super(SponsorBenefitsInlineFormSet, self)._construct_form(i, **kwargs)

        # only include the relevant data fields for this benefit type
        fields = form.instance.data_fields()
        form.fields = dict((k, v) for (k, v) in form.fields.items() if k in fields + ["id"])
        for field in fields:
            # don't need a label, the form template will label it with the benefit name
            form.fields[field].label = ""

            # provide word limit as help_text
            if form.instance.benefit.type in ["text", "richtext"] and form.instance.max_words:
                form.fields[field].help_text = u"maximum %s words" % form.instance.max_words

            # use admin file widget that shows currently uploaded file
            if field == "upload":
                form.fields[field].widget = AdminFileWidget()

        return form


SponsorBenefitsFormSet = inlineformset_factory(
    Sponsor, SponsorBenefit,
    formset=SponsorBenefitsInlineFormSet,
    can_delete=False, extra=0,
    fields=["text", "upload"]
)


class SponsorEmailForm(forms.Form):
    from_ = forms.EmailField(widget=forms.TextInput(attrs={'class': 'fullwidth-input'}))
    cc = forms.CharField(help_text=_(u"(comma-separated addresses)"),
                         required=False,
                         widget=forms.TextInput(attrs={'class': 'fullwidth-input'}))
    bcc = forms.CharField(help_text=_(u"(comma-separated addresses)"),
                          required=False,
                          widget=forms.TextInput(attrs={'class': 'fullwidth-input'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'fullwidth-input'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'fullwidth-textarea'}))
