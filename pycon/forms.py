from django import forms
from django.utils.translation import ugettext_lazy as _

from markedit.widgets import MarkEdit

from pycon.models import (PyConProposalCategory, PyConTalkProposal,
                          PyConTutorialProposal, PyConPosterProposal,
                          PyConLightningTalkProposal)
from pycon.models import PyConSponsorTutorialProposal


class PyConProposalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PyConProposalForm, self).__init__(*args, **kwargs)
        self.fields["category"] = forms.ModelChoiceField(
            queryset=PyConProposalCategory.objects.order_by("name")
        )

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                _(u"The description must be less than 400 characters")
            )
        return value


class PyConTalkProposalForm(PyConProposalForm):

    class Meta:
        model = PyConTalkProposal
        fields = [
            "title",
            "category",
            "duration",
            "description",
            "audience",
            "audience_level",
            "perceived_value",
            "abstract",
            "outline",
            "additional_notes",
            "additional_requirements",
            "recording_release",
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "description": forms.Textarea(attrs={'rows': '3'}),
            "audience": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "perceived_value": forms.Textarea(attrs={'rows': '3'}),
            "abstract": MarkEdit(),
            "outline": MarkEdit(),
            "additional_notes": MarkEdit(attrs={'rows': '3'}),
            "additional_requirements": forms.Textarea(attrs={'rows': '3'}),
        }


class PyConLightningTalkProposalForm(PyConProposalForm):

    def __init__(self, *args, **kwargs):
        super(PyConLightningTalkProposalForm, self).__init__(*args, **kwargs)
        self.fields['audience_level'].widget = forms.HiddenInput()
        self.fields['audience_level'].initial = PyConLightningTalkProposal.AUDIENCE_LEVEL_NOVICE

    class Meta:
        model = PyConLightningTalkProposal
        fields = [
            "title",
            "category",
            "description",
            "additional_notes",
            "additional_requirements",
            "audience_level",
            "recording_release",
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "description": forms.Textarea(attrs={'rows': '3'}),
            "additional_notes": MarkEdit(attrs={'rows': '3'}),
            "additional_requirements": forms.Textarea(attrs={'rows': '3'}),
        }


class PyConTutorialProposalForm(PyConProposalForm):

    class Meta:
        model = PyConTutorialProposal
        fields = [
            "title",
            "category",
            "audience_level",
            "domain_level",
            "description",
            "audience",
            "perceived_value",
            "abstract",
            "outline",
            "more_info",
            "additional_notes",
            "additional_requirements",
            "handout",
            "recording_release",
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "description": forms.Textarea(attrs={'rows': '3'}),
            "audience": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "perceived_value": forms.Textarea(attrs={'rows': '3'}),
            "abstract": MarkEdit(),
            "outline": MarkEdit(),
            "more_info": MarkEdit(),
            "additional_notes": MarkEdit(attrs={'rows': '3'}),
            "additional_requirements": forms.Textarea(attrs={'rows': '3'}),
        }


class PyConPosterProposalForm(PyConProposalForm):

    class Meta:
        model = PyConPosterProposal
        fields = [
            "title",
            "category",
            "audience_level",
            "description",
            "abstract",
            "additional_notes",
            "additional_requirements",
            "recording_release",
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "description": forms.Textarea(attrs={'rows': '3'}),
            "abstract": MarkEdit(),
            "additional_notes": MarkEdit(attrs={'rows': '3'}),
            "additional_requirements": forms.Textarea(attrs={'rows': '3'}),
        }


class PyConSponsorTutorialForm(PyConProposalForm):

    class Meta:
        model = PyConSponsorTutorialProposal
        fields = [
            "title",
            "description",
            "abstract",
            "additional_notes",
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'fullwidth-input'}),
            "description": forms.Textarea(attrs={'rows': '3'}),
            "abstract": MarkEdit(),
            "additional_notes": MarkEdit(attrs={'rows': '3'}),
        }
