from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from taggit.forms import TagField

from symposion.proposals.models import SupportingDocument

# @@@ generic proposal form


class AddSpeakerForm(forms.Form):

    email = forms.EmailField(
        label="Email address of new speaker (use their email address, not yours)"
    )

    def __init__(self, *args, **kwargs):
        self.proposal = kwargs.pop("proposal")
        super(AddSpeakerForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        value = self.cleaned_data["email"]
        if value.lower() == self.proposal.speaker.email.lower():
            raise forms.ValidationError(
                _("You have submitted the Proposal author's email address. Please" \
                " select another email address.")
            )
        exists = self.proposal.additional_speakers.filter(
            Q(user=None, invite_email=value) |
            Q(user__email=value)
        ).exists()
        if exists:
            raise forms.ValidationError(
                "This email address has already been invited to your talk proposal"
            )
        return value

class SupportingDocumentCreateForm(forms.ModelForm):

    class Meta:
        model = SupportingDocument
        fields = [
            "file",
            "description",
        ]


class ProposalTagsForm(forms.Form):
    tags = TagField(required=False,
                    help_text=_(u"Comma-separated list of tags"))
