from django.shortcuts import render

from django.contrib.auth.decorators import login_required

import account.views

import symposion.forms


class SignupView(account.views.SignupView):
    
    form_class = symposion.forms.SignupForm
    
    def create_user(self, form, commit=True):
        user_kwargs = {
            "first_name": form.cleaned_data["first_name"],
            "last_name": form.cleaned_data["last_name"]
        }
        return super(SignupView, self).create_user(form, commit=commit, **user_kwargs)


@login_required
def dashboard(request):
    return render(request, "dashboard.html")
