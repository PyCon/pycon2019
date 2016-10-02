from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _

from multi_email_field.forms import MultiEmailField

from pycon.sponsorship.models import Sponsor, SponsorBenefit, SponsorLevel


class SponsorDetailsForm(forms.ModelForm):
    contact_emails = MultiEmailField(
        help_text=_(u"Please enter one email address per line.")
    )

    class Meta:
        model = Sponsor
        fields = ["name",
                  "contact_name",
                  "contact_emails",
                  "contact_phone",
                  "contact_address",
                  "external_url",
                  "display_url",
                  "twitter_username",
                  "web_description",
                  "web_logo",
                  ]
        widgets = {
            'web_description': forms.widgets.Textarea(attrs={'cols': 40, 'rows': 5}),
        }


class SponsorApplicationForm(SponsorDetailsForm):

    class Meta(SponsorDetailsForm.Meta):
        fields = SponsorDetailsForm.Meta.fields + [
            "level",
            "wants_table",
            "wants_booth",
            "small_entity_discount",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        kwargs.update({
            "initial": {
                "contact_name": self.user.get_full_name(),
                "contact_emails": [self.user.email],
            }
        })
        super(SponsorApplicationForm, self).__init__(*args, **kwargs)
        # TODO: there should be a way to turn off each level as it
        # fills, instead of having to edit code. Plus, this should
        # really be a radio button, where the unavailable ones stay
        # visible but grayed out with "Full" or "Out" next to them.
        self.fields['level'].queryset = (
            SponsorLevel.objects
            # .exclude(name='Open Source and Community')
            # .exclude(name='Financial Aid Sponsor')
            # .exclude(name='Media')
            # .exclude(name='Patron')
            # .exclude(name='Silver')
            # .exclude(name='Gold')
            # .exclude(name='Platinum')
            # .exclude(name='Diamond')
            # .exclude(name='Keystone')
            )

    def save(self, commit=True):
        obj = super(SponsorApplicationForm, self).save(commit=False)
        obj.applicant = self.user
        if commit:
            obj.save()
        return obj



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
