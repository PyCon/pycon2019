from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from django.contrib.admin.views.decorators import staff_member_required

from boxes.forms import BoxForm
from boxes.models import Box


@staff_member_required
def box_edit(request, pk):

    box = get_object_or_404(Box, pk=pk)
    if request.method == "POST":
        
        form = BoxForm(request.POST, instance=box)
        if form.is_valid():
            form.save()
            return render_to_response("boxes/refresh.html", {})
    else:
        form = BoxForm(instance=box)
    ctx = {
        "form": form,
        "box": box,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("boxes/box_edit.html", ctx)


@staff_member_required
def box_create(request, label):

    if request.method == "POST":
        
        form = BoxForm(request.POST)
        if form.is_valid():
            box = form.save(commit=False)
            box.label = label
            box.created_by = request.user
            box.last_updated_by = request.user
            box.save()
            return render_to_response("boxes/refresh.html", {})
    else:
        form = BoxForm()
    ctx = {
        "form": form,
        "label": label
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("boxes/box_create.html", ctx)
