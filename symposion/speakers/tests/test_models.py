from __future__ import unicode_literals

from django.test import TestCase

from symposion.speakers.models import get_photo_path


class SpeakerModelTest(TestCase):
    def test_speaker_photo_filename(self):
        # A filename with unicode
        filename = '\u0141ukasz Langa.png'
        out = get_photo_path(None, filename)
        # We put them under speaker_photos/
        self.assertTrue(out.startswith('speaker_photos/'))
        # We preserve the extension
        self.assertTrue(out.endswith('.png'))
        # We're not doubling the dot
        self.assertFalse(out.endswith('..png'))
        # The result is ASCII
        out.encode('ASCII')
