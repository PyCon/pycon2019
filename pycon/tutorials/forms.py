from django import forms
from django.forms import Textarea

from pycon.tutorials.models import PyConTutorialMessage


class TutorialMessageForm(forms.ModelForm):
    class Meta:
        model = PyConTutorialMessage
        fields = [
            "message"
        ]
        widgets = {
            'message': Textarea(attrs={'class': 'fullwidth-textarea'}),
        }


class BulkEmailForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=Textarea(attrs={'class': 'fullwidth-textarea'}))
