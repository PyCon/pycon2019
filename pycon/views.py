import os
import shutil
from StringIO import StringIO
from uuid import uuid4
from zipfile import ZipFile

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from pycon.models import SpecialEvent
from pycon.program_export import export


def program_export(request):
    folder = '/tmp/{0}/'.format(uuid4())
    try:
        export(folder)
        s = StringIO()
        z = ZipFile(s, "w")
        for dirpath, dirs, files in os.walk(folder):
            for f in files:
                fn = os.path.join(dirpath, f)
                z.write(fn, "program_export/" + fn.split(folder, 1)[1])
        z.close()
        response = HttpResponse(s.getvalue(), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = 'attachment; filename=program_export.zip'
        return response
    finally:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except OSError:
                pass


def special_event(request, slug):
    """Special event detail page"""
    event = get_object_or_404(SpecialEvent, slug=slug, published=True)
    return render(request, "special_event.html", {
        'event': event,
        'page': {
            'title': event.name,
        }
    })
