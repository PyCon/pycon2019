import hashlib

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from constance import config

from djangosecure.decorators import frame_deny_exempt


@login_required
def cte_registration_start(request):
    return render(request, "registration/register.html")


@login_required
@frame_deny_exempt
def cte_registration_login(request):
    salt = config.CTE_SECRET
    token = hashlib.sha1(str(request.user.pk) + salt).hexdigest()
    return render(request, "registration/login.html", {
        "token": token,
    })
