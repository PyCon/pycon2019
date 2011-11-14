import hashlib

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from constance import config


def cte_login(request):
    
    salt = config.CTE_SECRET
    token = hashlib.sha1(str(request.user.id) + salt).hexdigest()
    ctx = {"token": token}

    return render_to_response("registration/login.html", RequestContext(request, ctx))
