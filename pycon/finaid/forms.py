from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea, Select
from django.utils.translation import ugettext_lazy as _

from .models import FinancialAidApplication, FinancialAidMessage, \
    FinancialAidReviewData, FinancialAidEmailTemplate, Receipt


def validate_is_checked(value):
    if not value:
        raise ValidationError(
            _('Please read the page, then click this box')
        )


class FinancialAidApplicationForm(forms.ModelForm):
    i_have_read = forms.BooleanField(
        label='I have read the <a href="https://us.pycon.org/2017/financial-assistance/">Financial Assistance</a> page',
        required=False,         # so our own validator gets called
        validators=[validate_is_checked],
    )
    class Meta:
        model = FinancialAidApplication
        fields = [
            'i_have_read',
            'first_time',
            'amount_requested',
            'international',
            'travel_plans',
            'profession',
            'involvement',
            'what_you_want',
            'experience_level',
            'presenting',
            'presented',
            'pyladies_grant_requested',
        ]
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
        }
        help_texts = {
            'experience_level': (
                'We welcome people of all experience levels.'
                ' What is your experience level with Python?'
            ),
            'international': (
                'Check the box if you will be traveling internationally,'
                ' or from anywhere outside of the continental United States.'
            ),
            'involvement': (
                'Describe your involvement in any open source projects'
                ' or Python communities, local or international.'
            ),
            'profession': (
                'What is your career? If you are a student,'
                ' what is the name of the school you are attending?'
            ),
            'pyladies_grant_requested': (
                "Would you like to be considered for a PyLadies grant?"
                " (For women."
                " All trans and non-binary people are also eligible.)"
            ),
        }


class FinancialAidReviewForm(forms.ModelForm):

    class Meta:
        model = FinancialAidReviewData
        fields = ['status', 'amount', 'grant_letter_sent', 'cash_check',
                  'notes', 'disbursement_notes',
                  'promo_code']
        widgets = {
            'notes': Textarea(
                attrs={'cols': 80, 'rows': 5,
                       'class': 'fullwidth-textarea'}),
            'travel_preferred_disbursement': Textarea(
                attrs={'cols': 80, 'rows': 5,
                       'class': 'fullwidth-textarea'}),
            'grant_letter_sent': Select(
                choices=(
                    (False, _("No")),
                    (True, _("Yes")),
                )
            ),
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


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ["description", "amount", "receipt_image"]
