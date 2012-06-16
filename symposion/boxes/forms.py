from django import forms

from boxes.models import Box


class BoxForm(forms.ModelForm):
    
    class Meta:
        model = Box
        fields = ["content"]
