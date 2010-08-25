from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from sponsors.models import Sponsor, SponsorBenefit


class SponsorApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(SponsorApplicationForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Sponsor
        fields = ["name", "contact_name", "contact_email"]
    
    def save(self, commit=True):
        obj = super(SponsorApplicationForm, self).save(commit=False)
        obj.applicant = self.user
        if commit:
            obj.save()
        return obj


class SponsorDetailsForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ["name", "external_url",
                  "contact_name", "contact_email"]


class SponsorBenefitsInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(SponsorBenefitsInlineFormSet, self)._construct_form(i, **kwargs)

        # only include the relevant data field for this benefit type
        form.fields = dict((k, v) for (k, v) in form.fields.items()
                           if k in form.instance.data_fields() + ['id'])

        return form
        

SponsorBenefitsFormSet = inlineformset_factory(Sponsor, SponsorBenefit,
                                               formset=SponsorBenefitsInlineFormSet,
                                               can_delete=False, extra=0,
                                               fields=['text', 'upload'])
