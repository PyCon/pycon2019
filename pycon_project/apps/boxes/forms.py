from django import forms

from markitup.widgets import MarkItUpWidget

from boxes.models import Box


class BoxForm(forms.ModelForm):
    
    content = forms.CharField(widget=MarkItUpWidget())
    
    class Meta:
        model = Box
        fields = ["content"]
