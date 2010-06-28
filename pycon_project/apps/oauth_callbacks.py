from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from pinax.apps.account.forms import SignupForm as PinaxSignupForm
from pinax.apps.account.utils import get_default_redirect, user_display

from oauth_access.access import OAuthAccess


def twitter_callback(request, access, token):
    
    if not request.user.is_authenticated():
        url = "https://twitter.com/account/verify_credentials.json"
        user_data = access.make_api_call("json", url, token)
        user = access.lookup_user(identifier=user_data["screen_name"])
        if user is None:
            request.session["oauth_signup_data"] = {
                "token": token,
                "user_data": user_data,
            }
            return redirect(
                reverse(
                    "oauth_access_finish_signup", kwargs={
                        "service": access.service
                    }
                )
            )
        else:
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
    else:
        user = request.user
    redirect_to = get_default_redirect(request)
    access.persist(user, token)
    return redirect(redirect_to)


def facebook_callback(request, access, token):
    
    if not request.user.is_authenticated():
        user_data = access.make_api_call("json", "https://graph.facebook.com/me", token)
        user = access.lookup_user(identifier=user_data["id"])
        if user is None:
            request.session["oauth_signup_data"] = {
                "token": token,
                "user_data": user_data,
            }
            return redirect(
                reverse(
                    "oauth_access_finish_signup", kwargs={
                        "service": access.service
                    }
                )
            )
        else:
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
    else:
        user = request.user
    redirect_to = get_default_redirect(request)
    access.persist(user, token)
    return redirect(redirect_to)


class SignupForm(PinaxSignupForm):
    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields["password1"]
        del self.fields["password2"]


def finish_signup(request, service):
    
    access = OAuthAccess(service)
    data = request.session.get("oauth_signup_data", None)
    ctx = {}
    
    if data["token"]:
        if request.method == "POST":
            form = SignupForm(request.POST)
            
            # @@@ pulled from Pinax (a class based view would be awesome here
            # to reduce duplication)
            if form.is_valid():
                success_url = get_default_redirect(request)
                user = form.save(request=request)
                if service == "twitter":
                    identifier = data["user_data"]["screen_name"]
                elif service == "facebook":
                    identifier = data["user_data"]["id"]
                access.persist(user, data["token"], identifier=identifier)
                # del request.session["oauth_signup_data"]
                if settings.ACCOUNT_EMAIL_VERIFICATION:
                    return render_to_response("account/verification_sent.html", {
                        "email": form.cleaned_data["email"],
                    }, context_instance=RequestContext(request))
                else:
                    form.login(request, user)
                    messages.add_message(request, messages.SUCCESS,
                        ugettext("Successfully logged in as %(user)s.") % {
                            "user": user_display(user)
                        }
                    )
                    return redirect(success_url)
        else:
            initial = {}
            if service == "twitter":
                username = data["user_data"]["screen_name"]
                if not User.objects.filter(username=username).exists():
                    initial["username"] = data["user_data"]["screen_name"]
                else:
                    ctx["username_taken"] = username
            form = SignupForm(initial=initial)
        
        ctx.update({
            "service": service,
            "form": form,
        })
        ctx = RequestContext(request, ctx)
        return render_to_response("oauth_access/finish_signup.html", ctx)
    else:
        return HttpResponse("no token!")
