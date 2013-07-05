from django import forms

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
                u"The description must be less than 400 characters"
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
            "slide_deck",
            "recording_release",
        ]
        widgets = {
            "abstract": MarkEdit(),
            "additional_notes": MarkEdit(),
            "outline": MarkEdit(),
        }


class PyConLightningTalkProposalForm(PyConProposalForm):

    def __init__(self, *args, **kwargs):
        super(PyConLightningTalkProposalForm, self).__init__(*args, **kwargs)
        self.fields['duration'].widget.attrs['readonly'] = True
        # TODO: This is a hack to populate the field...
        self.fields['category'].widget = forms.HiddenInput()
        self.fields['category'].initial = PyConProposalCategory.objects.all()[0]
        self.fields['audience_level'].widget = forms.HiddenInput()
        self.fields['audience_level'].initial = PyConLightningTalkProposal.AUDIENCE_LEVEL_NOVICE

    class Meta:
        model = PyConLightningTalkProposal
        fields = [
            "title",
            "category",
            "duration",
            "description",
            "additional_notes",
            "additional_requirements",
            "audience_level",
            "slide_deck",
            "recording_release",
        ]
        widgets = {
            "additional_notes": MarkEdit(),
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
            "slide_deck",
            "handout",
            "recording_release",
        ]
        widgets = {
            "abstract": MarkEdit(),
            "outline": MarkEdit(),
            "more_info": MarkEdit(),
            "additional_notes": MarkEdit(),
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
            "abstract": MarkEdit(),
            "additional_notes": MarkEdit(),
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
            "abstract": MarkEdit(),
            "additional_notes": MarkEdit(),
        }
