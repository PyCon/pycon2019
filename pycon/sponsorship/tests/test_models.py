from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from symposion.conference.models import current_conference, Conference

from ..models import Benefit, Sponsor, SponsorBenefit, SponsorLevel


class TestBenefitValidation(TestCase):
    """
    It should not be possible to save a SponsorBenefit if it has the
    wrong kind of data in it - e.g. a text-type benefit cannot have
    an uploaded file, and vice-versa.
    """

    def setUp(self):
        # we need a sponsor
        Conference.objects.get_or_create(pk=settings.CONFERENCE_ID)
        conference = current_conference()
        self.sponsor_level = SponsorLevel.objects.create(
            conference=conference, name="Lead", cost=1)
        self.sponsor = Sponsor.objects.create(
            name="Big Daddy",
            level=self.sponsor_level,
        )

        # Create our benefit types
        self.text_type = Benefit.objects.create(name="text", type="text")
        self.file_type = Benefit.objects.create(name="file", type="file")
        self.weblogo_type = Benefit.objects.create(name="log", type="weblogo")
        self.simple_type = Benefit.objects.create(name="simple", type="simple")

    def validate(self, should_work, benefit_type, upload, text):
        obj = SponsorBenefit(
            benefit=benefit_type,
            sponsor=self.sponsor,
            upload=upload,
            text=text
        )
        if should_work:
            obj.save()
        else:
            with self.assertRaises(ValidationError):
                obj.save()

    def test_text_has_text(self):
        self.validate(True, self.text_type, upload=None, text="Some text")

    def test_text_has_upload(self):
        self.validate(False, self.text_type, upload="filename", text='')

    def test_text_has_both(self):
        self.validate(False, self.text_type, upload="filename", text="Text")

    def test_file_has_text(self):
        self.validate(False, self.file_type, upload=None, text="Some text")

    def test_file_has_upload(self):
        self.validate(True, self.file_type, upload="filename", text='')

    def test_file_has_both(self):
        self.validate(False, self.file_type, upload="filename", text="Text")

    def test_weblogo_has_text(self):
        self.validate(False, self.weblogo_type, upload=None, text="Some text")

    def test_weblogo_has_upload(self):
        self.validate(True, self.weblogo_type, upload="filename", text='')

    def test_weblogo_has_both(self):
        self.validate(False, self.weblogo_type, upload="filename", text="Text")

    def test_simple_has_neither(self):
        self.validate(True, self.simple_type, upload=None, text='')

    def test_simple_has_text(self):
        self.validate(True, self.simple_type, upload=None, text="Some text")

    def test_simple_has_upload(self):
        self.validate(False, self.simple_type, upload="filename", text='')

    def test_simple_has_both(self):
        self.validate(False, self.simple_type, upload="filename", text="Text")
