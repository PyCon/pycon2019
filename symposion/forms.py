from django import forms

import account.forms


class SignupForm(account.forms.SignupForm):
    
    first_name = forms.CharField()
    last_name = forms.CharField()