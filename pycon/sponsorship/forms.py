import re
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.core.files.images import get_image_dimensions
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _

from multi_email_field.forms import MultiEmailField

from pycon.sponsorship.models import Sponsor, SponsorBenefit, SponsorLevel, SponsorPackage


WEB_LOGO_TYPES = ['png', 'jpg']
PRINT_LOGO_TYPES = ['svg', 'eps']


def strip(text):
    return u' '.join(text.strip().split())


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
                  "print_logo",
                  ]
        widgets = {
            'web_description': forms.widgets.Textarea(attrs={'cols': 40, 'rows': 5}),
        }

    def clean_web_logo(self):
        image_file = self.cleaned_data.get("web_logo")
        if image_file:
            if not image_file.name.split('.')[-1].lower() in WEB_LOGO_TYPES:
                raise forms.ValidationError(
                    "Your file extension was not recognized, please submit "
                    "one of: {}".format(', '.join(WEB_LOGO_TYPES))
                )
            w, h = get_image_dimensions(image_file)
            if w < 768 and h < 768:
                raise forms.ValidationError(
                    "Smallest dimension must be no less than 768px, "
                    "submitted image had dimensions {}x{}".format(w, h)
                )
        else:
            raise forms.ValidationError("You must supply a web logo file")
        return image_file

    def clean_print_logo(self):
        image_file = self.cleaned_data.get("print_logo")
        if image_file:
            if not image_file.name.split('.')[-1].lower() in PRINT_LOGO_TYPES:
                raise forms.ValidationError(
                    "Your file extension was not recognized, please submit "
                    "one of: {}".format(', '.join(PRINT_LOGO_TYPES))
                )
        return image_file


class SponsorApplicationForm(SponsorDetailsForm):
    packages = forms.ModelMultipleChoiceField(
        label=_(u"\xc0 la carte sponsorship packages"),
        widget=forms.CheckboxSelectMultiple,
        queryset=SponsorPackage.objects.filter(available=True),
        required=False,
    )

    class Meta(SponsorDetailsForm.Meta):
        fields = SponsorDetailsForm.Meta.fields + [
            "level",
            "packages",
            "wants_table",
            "wants_booth",
            "small_entity_discount",
        ]
        help_texts = {
            'web_description': strip(
                u"""
                Your description can be up to 100 words long.
                """
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        kwargs.update({
            "initial": {
                "contact_name": self.user.get_full_name(),
                "contact_emails": [self.user.email],
            }
        })
        super(SponsorApplicationForm, self).__init__(*args, **kwargs)
        self.fields['level'].queryset = SponsorLevel.objects.exclude(
            available=False)

    def clean_web_description(self):
        value = self.cleaned_data['web_description']
        word_count = len(re.findall(r"[-\w']+", value.lower()))
        if word_count > 100:
            raise forms.ValidationError(
                _(u"Your description is {} words long;"
                  " please reduce it to 100 or less.".format(word_count))
            )
        return value

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
    sample_subject = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'fullwidth-input',
            'readonly': True,
            'style': 'background-color: #ddd',
        }),
    )
    sample_body = forms.CharField(
        help_text=_(u"""
            You can keep editing the body and hitting Send
            until you love how this preview looks.
            Then, press Send one final time!
        """),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'fullwidth-textarea',
            'readonly': True,
            'style': 'background-color: #ddd',
        }),
    )
