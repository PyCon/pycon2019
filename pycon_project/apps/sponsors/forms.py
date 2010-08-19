from django import forms

from sponsors.models import Sponsor


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
