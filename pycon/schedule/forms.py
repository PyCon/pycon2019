from django import forms

from .models import SlidesUpload

class SlidesUploadForm(forms.ModelForm):

    class Meta:
        model = SlidesUpload
        fields = ["slides"]
