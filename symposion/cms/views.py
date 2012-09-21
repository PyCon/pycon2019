from django.http import Http404
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import Page
from .forms import PageForm


def can_edit(page, user):
    if page and page.is_community:
        return True
    else:
        return user.has_perm("cms.change_page")


def page(request, path):
    
    try:
        page = Page.published.get(path=path)
    except Page.DoesNotExist:
        page = None
    
    editable = can_edit(page, request.user)
    
    if page is None:
        if editable:
            return redirect("cms_page_edit", path=path)
        else:
            raise Http404
    
    return render(request, "cms/page_detail.html", {
        "page": page,
        "editable": editable,
    })


@login_required
def page_edit(request, path):
    
    try:
        page = Page.published.get(path=path)
    except Page.DoesNotExist:
        page = None
    
    if not can_edit(page, request.user):
        raise Http404
    
    if request.method == "POST":
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save(commit=False)
            page.path = path
            page.save()
            return redirect(page)
        else:
            print form.errors
    else:
        form = PageForm(instance=page, initial={"path": path})
    
    return render(request, "cms/page_edit.html", {
        "path": path,
        "form": form
    })
