from cStringIO import StringIO
import os
import shutil
import tempfile
from zipfile import ZipFile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from pycon.sponsorship.models import Benefit, SponsorBenefit, Sponsor, \
    SponsorLevel
from symposion.conference.models import current_conference


class TestSponsorZipDownload(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='joe',
                                             email='joe@example.com',
                                             password='joe')
        self.user.is_staff = True
        self.user.save()
        self.url = reverse("sponsor_zip_logos")
        self.assertTrue(self.client.login(username='joe@example.com',
                                          password='joe'))

        # we need a sponsor
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

    def validate_response(self, rsp, names_and_sizes):
        # Ensure a response from the view looks right, contains a valid
        # zip archive, has files with the right names and sizes.
        self.assertEqual("application/zip", rsp['Content-type'])
        self.assertEqual('attachment; filename="pycon2014_sponsorlogos.zip"',
                         rsp['Content-Disposition'])
        zipfile = ZipFile(StringIO(rsp.content), "r")
        # Check out the zip - testzip() returns None if no errors found
        self.assertIsNone(zipfile.testzip())
        # Compare contents to what is expected
        infolist = zipfile.infolist()
        self.assertEqual(len(names_and_sizes), len(infolist))
        for info, name_and_size in zip(infolist, names_and_sizes):
            name, size = name_and_size
            self.assertEqual(name, info.filename)
            self.assertEqual(size, info.file_size)

    def make_temp_file(self, name, size=0):
        # Create a temp file with the given name and size under self.temp_dir
        path = os.path.join(self.temp_dir, name)
        with open(path, "wb") as f:
            f.write(size * "x")

    def test_must_be_logged_in(self):
        # Must be logged in to use the view
        # If not logged in, doesn't redirect, just serves up a login view
        self.client.logout()
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        self.assertIn("""<body class="login">""", rsp.content)

    def test_must_be_staff(self):
        # Only staff can use the view
        # If not staff, doesn't show error, just serves up a login view
        self.user.is_staff = False
        self.user.save()
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        self.assertIn("""<body class="login">""", rsp.content)

    def test_no_files(self):
        # If there are no sponsor files, we still work
        rsp = self.client.get(self.url)
        self.validate_response(rsp, [])

    def test_different_benefit_types(self):
        # We only get files from benefits of type `file` and `weblogo`
        try:
            # Create a temp dir for media files
            self.temp_dir = tempfile.mkdtemp()
            with override_settings(MEDIA_ROOT=self.temp_dir):

                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.text_type,
                    text="Foo!"
                )

                self.make_temp_file("file1", 10)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.file_type,
                    upload="file1"
                )

                self.make_temp_file("file2", 20)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.weblogo_type,
                    upload="file2"
                )
                rsp = self.client.get(self.url)
                self.validate_response(rsp, [('file1', 10), ('file2', 20)])
        finally:
            if hasattr(self, 'temp_dir'):
                # Clean up any temp media files
                shutil.rmtree(self.temp_dir)
