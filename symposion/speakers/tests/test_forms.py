from __future__ import unicode_literals

import StringIO

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from symposion.speakers.forms import SpeakerForm


class SpeakerFormTest(TestCase):
    def test_nonascii_name(self):
        name = '\u0141ukasz Langa'
        png_file = StringIO.StringIO()
        # Use PIL Image to create new png and pdf files
        Image.new('RGB', size=(50, 50), color=(256, 0, 0)).save(png_file, 'png')
        png_file.seek(0)
        # Django-friendly ContentFiles
        file = SimpleUploadedFile(name + '.png', png_file.read())
        form = SpeakerForm(
            data={
                'name': name,
                'biography': name,
                '': None,
                'twitter_username': '',
            },
            files={'photo': file},
        )
        self.assertTrue(
            form.is_valid(),
            msg=form.errors
        )
        form.save()
