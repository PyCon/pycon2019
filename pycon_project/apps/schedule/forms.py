from django import forms

from schedule.models import Plenary, Recess, Presentation


class PlenaryForm(forms.ModelForm):
    class Meta:
        model = Plenary
        exclude = ["slot"]


class RecessForm(forms.ModelForm):
    class Meta:
        model = Recess
        exclude = ["slot"]


class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        exclude = ["slot"]