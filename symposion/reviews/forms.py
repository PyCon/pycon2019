from django import forms

from symposion.reviews.models import Review, Comment, ProposalMessage, VOTES


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["vote", "comment"]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["vote"] = forms.ChoiceField(
            widget=forms.RadioSelect(),
            choices=VOTES.CHOICES
        )


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class SpeakerCommentForm(forms.ModelForm):
    class Meta:
        model = ProposalMessage
        fields = ["message"]


class BulkPresentationForm(forms.Form):
    talk_ids = forms.CharField(
        max_length=500,
        help_text="Provide a comma seperated list of talk ids to accept."
    )
