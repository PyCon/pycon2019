from django import forms

from markedit.widgets import MarkEdit

from .models import Page


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ["title", "body", "path"]
        widgets = {
            "path": forms.HiddenInput(),
            "body": MarkEdit(),
        }


class FileUploadForm(forms.Form):

    file = forms.FileField()
