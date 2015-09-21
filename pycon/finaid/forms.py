import os
from django import forms
from django.forms import Textarea, Select
from django.utils.translation import ugettext_lazy as _

from .models import FinancialAidApplication, FinancialAidMessage, \
    FinancialAidReviewData, FinancialAidEmailTemplate, Receipt


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
    def clean(self, *args, **kwargs):
        """We require the receipt image field to be the correct format."""
        cleaned_data = super(ReceiptForm, self).clean()
        receipt_field = cleaned_data.get("receipt_image")
        accepted_formats = ['.bmp', '.jpeg', '.jpg', '.png', '.pdf']
        if receipt_field is not None:
            if os.path.splitext(receipt_field.file.name)[1] not in accepted_formats:
                raise forms.ValidationError(
                    "File format was not accepted. The only acceptable formats "
                    "are: .bmp, .jpeg, .jpg, .png, .pdf.")
        else:
            raise forms.ValidationError("No receipt image uploaded.")

    class Meta:
        model = Receipt
        fields = ["description", "amount", "receipt_image"]
