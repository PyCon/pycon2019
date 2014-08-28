from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _

from .models import FinancialAidApplication, FinancialAidMessage, \
    FinancialAidReviewData, FinancialAidEmailTemplate


class FinancialAidApplicationForm(forms.ModelForm):
    class Meta:
        model = FinancialAidApplication
        exclude = ["timestamp", "user", "status"]
        widgets = {
            'travel_plans': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea',
                       'maxlength': 1024}),
            'what_you_do': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea',
                       'maxlength': 500}),
            'involvement': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea',
                       'maxlength': 1024}),
            'what_you_want': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea',
                       'maxlength': 500}),
            'portfolios': Textarea(
                attrs={'cols': 80, 'rows': 3,
                       'class': 'fullwidth-textarea',
                       'maxlength': 500}),
            'use_of_python': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea',
                       'maxlength': 500}),
            'experience_level': Textarea(
                attrs={'cols': 80, 'rows': 2,
                       'class': 'fullwidth-textarea',
                       'maxlength': 200}),
        }


class FinancialAidReviewForm(forms.ModelForm):

    class Meta:
        model = FinancialAidReviewData
        widgets = {
            'notes': Textarea(
                attrs={'cols': 80, 'rows': 5,
                       'class': 'fullwidth-textarea'}),
            'travel_preferred_disbursement': Textarea(
                attrs={'cols': 80, 'rows': 5,
                       'class': 'fullwidth-textarea'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = FinancialAidMessage
        fields = [
            "message"
        ]
        widgets = {
            'message': Textarea(attrs={'class': 'fullwidth-textarea'}),
        }


class ReviewerMessageForm(forms.ModelForm):
    class Meta:
        model = FinancialAidMessage
        fields = [
            "visible",
            "message"
        ]
        widgets = {
            'message': Textarea(attrs={'class': 'fullwidth-textarea'}),
        }


class BulkEmailForm(forms.Form):
    subject = forms.CharField()
    template = forms.ModelChoiceField(
        queryset=FinancialAidEmailTemplate.objects.all(),
        empty_label=u"Pick a bulk mail template to use",
    )
