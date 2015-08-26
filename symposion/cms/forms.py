from django import forms
from django.conf import settings

from markedit.widgets import MarkEdit

from .models import Page


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ["title", "body", "body_fr", "path"]
        widgets = {
            "path": forms.HiddenInput(),
            "body": MarkEdit(),
            "body_fr": MarkEdit(),
        }
        if not settings.USE_I18N:
            fields.remove('body_fr')
            del widgets['body_fr']


class FileUploadForm(forms.Form):

    file = forms.FileField()
