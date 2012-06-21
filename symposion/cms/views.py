from django.http import Http404
from django.shortcuts import render
from django.template import RequestContext

from .models import Page


def page(request, path):
    
    try:
        page = Page.published.get(path=path)
    except Page.DoesNotExist:
        raise Http404
    
    return render(request, "cms/page_detail.html", {
        "page": page,
    })
