from django import forms
from django.contrib.auth.models import User

from symposion.utils.signup import generate_username


class GroupRegistrationForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField()

    def create_user(self):
        """Create a new user with an unusable password."""
        email = User.objects.normalize_email(self.cleaned_data['email'])
        user = User(
            username=generate_username(email),
            email=email,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
        )
        user.set_unusable_password()
        user._disable_account_creation = True
        user.save()
        return user

    def save(self):
        email = self.cleaned_data['email']
        existing = User.objects.filter(email__iexact=email)
        if existing:
            created = False
            user = existing[0]
        else:
            created = True
            user = self.create_user()
        return created, user
