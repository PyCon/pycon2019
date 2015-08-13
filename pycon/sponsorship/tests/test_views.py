from cStringIO import StringIO
import os
import shutil
import tempfile
from zipfile import ZipFile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from symposion.conference.models import current_conference, Conference

from pycon.tests.base import ViewTestMixin
from pycon.tests.factories import UserFactory

from ..models import Benefit, Sponsor, SponsorBenefit, SponsorLevel

from .factories import SponsorLevelFactory


# Tiny image file for testing
TEST_IMAGE_FILENAME = os.path.join(os.path.dirname(__file__), 'colormap.gif')
TEST_IMAGE = open(TEST_IMAGE_FILENAME, "rb").read()
# Where the fixtures are
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), '../../../fixtures')


class TestSponsorZipDownload(TestCase):
    fixtures = [
        os.path.join(FIXTURE_DIR, 'conference.json'),
        os.path.join(FIXTURE_DIR, 'sponsorship_levels.json'),
        os.path.join(FIXTURE_DIR, 'sponsorship_benefits.json'),
    ]

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
        Conference.objects.get_or_create(pk=settings.CONFERENCE_ID)
        conference = current_conference()
        self.sponsor_level = SponsorLevel.objects.create(
            conference=conference, name="Lead", cost=1, order=199)
        self.sponsor = Sponsor.objects.create(
            name="Big Daddy",
            level=self.sponsor_level,
            active=True,
        )

        # Create our benefits, of various types
        self.text_benefit = Benefit.objects.create(name="text", type="text")
        self.file_benefit = Benefit.objects.create(name="file", type="file")
        self.printlogo_benefit = Benefit.objects.get(
            name="Print logo", type="file")
        self.advertisement_benefit = Benefit.objects.get(
            name="Advertisement", type="file")

    def validate_response(self, rsp, names_and_sizes):
        # Ensure a response from the view looks right, contains a valid
        # zip archive, has files with the right names and sizes.
        self.assertEqual("application/zip", rsp['Content-type'])
        prefix = settings.CONFERENCE_URL_PREFIXES[settings.CONFERENCE_ID]

        self.assertEqual(
            'attachment; filename="pycon_%s_sponsorlogos.zip"' % prefix,
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
        # If not logged in, redirects to a login view
        self.client.logout()
        rsp = self.client.get(self.url, follow=True)
        self.assertEqual(200, rsp.status_code)
        self.assertIn("""<body class="login">""", rsp.content)

    def test_must_be_staff(self):
        # Only staff can use the view
        # If not staff, doesn't show error, just redirects to a login view
        # Also, the dashboard doesn't show the download button
        self.user.is_staff = False
        self.user.save()
        rsp = self.client.get(self.url, follow=True)
        self.assertEqual(200, rsp.status_code)
        self.assertIn("""<body class="login">""", rsp.content)
        rsp = self.client.get(reverse('dashboard'))
        self.assertNotIn(self.url, rsp.content)

    def test_no_files(self):
        # If there are no sponsor files, we still work
        # And the dashboard shows our download button
        rsp = self.client.get(self.url)
        self.validate_response(rsp, [])
        rsp = self.client.get(reverse('dashboard'))
        self.assertIn(self.url, rsp.content)

    def test_different_benefit_types(self):
        # We only get files from the benefits named "Print logo" and "Web logo"
        # And we ignore any non-existent files
        try:
            # Create a temp dir for media files
            self.temp_dir = tempfile.mkdtemp()
            with override_settings(MEDIA_ROOT=self.temp_dir):

                # Give our sponsor some benefits
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.text_benefit,
                    text="Foo!"
                )

                self.make_temp_file("file1", 10)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.file_benefit,
                    upload="file1"
                )

                self.make_temp_file("file2", 20)
                self.sponsor.web_logo = "file2"
                self.sponsor.save()

                # Benefit whose file is missing from the disk
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.printlogo_benefit,
                    upload="file3"
                )

                # print logo benefit
                self.make_temp_file("file4", 40)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.printlogo_benefit,
                    upload="file4"
                )

                self.make_temp_file("file5", 50)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.advertisement_benefit,
                    upload="file5"
                )

                rsp = self.client.get(self.url)
                expected = [
                    ('web_logos/lead/big_daddy/file2', 20),
                    ('print_logos/lead/big_daddy/file4', 40),
                    ('advertisement/lead/big_daddy/file5', 50)
                ]
                self.validate_response(rsp, expected)
        finally:
            if hasattr(self, 'temp_dir'):
                # Clean up any temp media files
                shutil.rmtree(self.temp_dir)

    def test_file_org(self):
        # The zip file is organized into directories:
        #  {print_logos,web_logos,advertisement}/<sponsor_level>/<sponsor_name>/<filename>

        # Add another sponsor at a different sponsor level
        conference = current_conference()
        self.sponsor_level2 = SponsorLevel.objects.create(
            conference=conference, name="Silly putty", cost=1, order=299)
        self.sponsor2 = Sponsor.objects.create(
            name="Big Mama",
            level=self.sponsor_level2,
            active=True,
        )
        #
        try:
            # Create a temp dir for media files
            self.temp_dir = tempfile.mkdtemp()
            with override_settings(MEDIA_ROOT=self.temp_dir):

                # Give our sponsors some benefits
                self.make_temp_file("file1", 10)
                self.sponsor.web_logo = "file1"
                self.sponsor.save()
                # print logo benefit
                self.make_temp_file("file2", 20)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.printlogo_benefit,
                    upload="file2"
                )
                # Sponsor 2
                self.make_temp_file("file3", 30)
                self.sponsor2.web_logo = "file3"
                self.sponsor2.save()
                # print logo benefit
                self.make_temp_file("file4", 42)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor2,
                    benefit=self.printlogo_benefit,
                    upload="file4"
                )
                # ad benefit
                self.make_temp_file("file5", 55)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor2,
                    benefit=self.advertisement_benefit,
                    upload="file5"
                )

                rsp = self.client.get(self.url)
                expected = [
                    ('web_logos/lead/big_daddy/file1', 10),
                    ('web_logos/silly_putty/big_mama/file3', 30),
                    ('print_logos/lead/big_daddy/file2', 20),
                    ('print_logos/silly_putty/big_mama/file4', 42),
                    ('advertisement/silly_putty/big_mama/file5', 55),
                ]
                self.validate_response(rsp, expected)
        finally:
            if hasattr(self, 'temp_dir'):
                # Clean up any temp media files
                shutil.rmtree(self.temp_dir)


class TestSponsorApply(ViewTestMixin, TestCase):
    fixtures = [
        os.path.join(FIXTURE_DIR, 'conference.json'),
        os.path.join(FIXTURE_DIR, 'sponsorship_levels.json'),
        os.path.join(FIXTURE_DIR, 'sponsorship_benefits.json'),
    ]
    url_name = 'sponsor_apply'

    def setUp(self):
        super(TestSponsorApply, self).setUp()
        Conference.objects.get_or_create(pk=settings.CONFERENCE_ID)
        self.user = UserFactory()
        self.login_user(self.user)
        self.sponsor_level = SponsorLevelFactory()
        self.data = {
            'name': 'Sponsor',
            'contact_name': self.user.get_full_name(),
            'contact_emails': [self.user.email],
            'contact_phone': '336-867-5309',
            'contact_address': '123 Main Street, Anytown, NC 90210',
            'level': self.sponsor_level.pk,
            'wants_table': True,
            'wants_booth': True,
            'web_logo': open(TEST_IMAGE_FILENAME, "rb"),
            'external_url': 'http://example.com',
            'web_description': 'Fools paradise',
        }

    def test_get_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 302)

    def test_post_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse(self.url_name), data=self.data)
        self.assertRedirectsToLogin(response)

    def test_get(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertFalse(response.context['form'].is_bound)

    def test_post_valid(self):
        response = self.client.post(reverse(self.url_name), data=self.data)
        self.assertRedirectsNoFollow(response, reverse('dashboard'))
        self.assertEqual(Sponsor.objects.count(), 1)
        sponsor = Sponsor.objects.first()
        self.assertEqual(self.data['web_description'], sponsor.web_description)
        self.assertEqual(TEST_IMAGE, sponsor.web_logo.read())

    def test_post_invalid(self):
        response = self.client.post(reverse(self.url_name), data={})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(response.context['form'].is_bound)
        self.assertFalse(response.context['form'].is_valid())

    def test_company_link_required(self):
        self.data.pop('external_url')
        response = self.client.post(reverse(self.url_name), data=self.data)
        self.assertIn('external_url', response.context['form'].errors)

    def test_web_description_required(self):
        self.data.pop('web_description')
        response = self.client.post(reverse(self.url_name), data=self.data)
        self.assertIn('web_description', response.context['form'].errors)

    def test_web_logo_required(self):
        self.data.pop('web_logo')
        response = self.client.post(reverse(self.url_name), data=self.data)
        self.assertIn('web_logo', response.context['form'].errors)
