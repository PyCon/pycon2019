from django import forms
from django.forms import Textarea

from .models import FinancialAidApplication


class FinancialAidApplicationForm(forms.ModelForm):
    class Meta:
        model = FinancialAidApplication
        exclude = ["timestamp", "user"]
        widgets = {
            'travel_plans': Textarea(attrs={'cols': 80, 'rows': 10}),
            'what_you_do': Textarea(attrs={'cols': 80, 'rows': 10}),
            'involvement': Textarea(attrs={'cols': 80, 'rows': 10}),
            'what_you_want': Textarea(attrs={'cols': 80, 'rows': 10}),
            'want_to_learn': Textarea(attrs={'cols': 80, 'rows': 10}),
            'portfolios': Textarea(attrs={'cols': 80, 'rows': 3}),
            'use_of_python': Textarea(attrs={'cols': 80, 'rows': 10}),
            'beginner_resources': Textarea(attrs={'cols': 80, 'rows': 5}),
            'experience_level': Textarea(attrs={'cols': 80, 'rows': 2}),
        }
