import hashlib

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from djangosecure.decorators import frame_deny_exempt

from constance import config


@login_required
@frame_deny_exempt
def cte_login(request):

    salt = config.CTE_SECRET
    token = hashlib.sha1(str(request.user.id) + salt).hexdigest()
    ctx = {
        "token": token,
        "REGISTRATION_URL": config.REGISTRATION_URL,
    }

    return render_to_response("registration/login.html",
                              RequestContext(request, ctx))
