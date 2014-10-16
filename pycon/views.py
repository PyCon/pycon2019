import os
from StringIO import StringIO
from uuid import uuid4
from zipfile import ZipFile

from django.http import HttpResponse

from pycon.program_export import export


def program_export(request):
    folder = '/tmp/{0}/'.format(uuid4())
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
