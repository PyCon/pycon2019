from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone']
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        
        self.fields.keyOrder = [
            "first_name",
            "last_name",
            "phone",
        ]
