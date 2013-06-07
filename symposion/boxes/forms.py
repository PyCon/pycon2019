from django import forms

from markedit.widgets import MarkEdit

from symposion.boxes.models import Box


class BoxForm(forms.ModelForm):

    class Meta:
        model = Box
        fields = ["content"]
        widgets = {
            "content": MarkEdit(),
        }
