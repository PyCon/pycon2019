from django import forms

from user_mailer.models import Campaign


class CampaignCreateForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ["created", "sent"]
