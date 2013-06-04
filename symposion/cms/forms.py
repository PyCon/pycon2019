from django import forms

from .models import Page


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ["title", "body", "path"]
        widgets = {
            "path": forms.HiddenInput(),
        }


class FileUploadForm(forms.Form):

    file = forms.FileField()
