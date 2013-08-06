from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from selectable import forms as selectable

from taggit.forms import TagField

from symposion.proposals.models import SupportingDocument

from .lookups import UserLookup

# @@@ generic proposal form


class AddSpeakerForm(forms.Form):

    email = selectable.AutoCompleteSelectField(
        lookup_class=UserLookup,
        allow_new=True,
        label="Email address of new speaker (use their email address, not yours)" \
              " If a User is not found for the supplied email, an invite will be sent" \
              " to the new speaker.",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.proposal = kwargs.pop("proposal")
        super(AddSpeakerForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        value = self.cleaned_data["email"]
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
