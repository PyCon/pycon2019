from django import forms
from django.forms import Textarea, DateInput

from .models import FinancialAidApplication, FinancialAidMessage


class FinancialAidApplicationForm(forms.ModelForm):
    class Meta:
        model = FinancialAidApplication
        exclude = ["timestamp", "user", "status"]
        widgets = {
            'hotel_arrival_date': DateInput(format='%Y-%m-%d'),
            'hotel_departure_date': DateInput(format='%Y-%m-%d'),
            'travel_plans': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea'}),
            'what_you_do': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea'}),
            'involvement': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea'}),
            'what_you_want': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea'}),
            'want_to_learn': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea'}),
            'portfolios': Textarea(
                attrs={'cols': 80, 'rows': 3,
                       'class': 'fullwidth-textarea'}),
            'use_of_python': Textarea(
                attrs={'cols': 80, 'rows': 10,
                       'class': 'fullwidth-textarea'}),
            'beginner_resources': Textarea(
                attrs={'cols': 80, 'rows': 5,
                       'class': 'fullwidth-textarea'}),
            'experience_level': Textarea(
                attrs={'cols': 80, 'rows': 2,
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
