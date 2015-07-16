from cStringIO import StringIO
from httplib import OK
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

from pycon.sponsorship.forms import SponsorBenefitsFormSet
from pycon.tests.base import ViewTestMixin
from pycon.tests.factories import UserFactory

from ..models import Benefit, Sponsor, SponsorBenefit, SponsorLevel, ContactEmail

from .factories import SponsorLevelFactory, SponsorFactory


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
        Conference.objects.get_or_create(pk=settings.CONFERENCE_ID)
        conference = current_conference()
        self.sponsor_level = SponsorLevel.objects.create(
            conference=conference, name="Lead", cost=1)
        self.sponsor = Sponsor.objects.create(
            name="Big Daddy",
            level=self.sponsor_level,
            active=True,
        )

        # Create our benefits, of various types
        self.text_benefit = Benefit.objects.create(name="text", type="text")
        self.file_benefit = Benefit.objects.create(name="file", type="file")
        # These names must be spelled exactly this way:
        self.weblogo_benefit = Benefit.objects.create(
            name="Web logo", type="weblogo")
        self.printlogo_benefit = Benefit.objects.create(
            name="Print logo", type="file")
        self.advertisement_benefit = Benefit.objects.create(
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
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.weblogo_benefit,
                    upload="file2"
                )

                # Benefit whose file is missing from the disk
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.weblogo_benefit,
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
            conference=conference, name="Silly putty", cost=1)
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
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.weblogo_benefit,
                    upload="file1"
                )
                # print logo benefit
                self.make_temp_file("file2", 20)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.printlogo_benefit,
                    upload="file2"
                )
                # Sponsor 2
                self.make_temp_file("file3", 30)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor2,
                    benefit=self.weblogo_benefit,
                    upload="file3"
                )
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
    url_name = 'sponsor_apply'

    def setUp(self):
        super(TestSponsorApply, self).setUp()
        conference, __ = Conference.objects.get_or_create(pk=settings.CONFERENCE_ID)
        self.user = UserFactory()
        self.login_user(self.user)
        self.sponsor_level = SponsorLevelFactory(conference=conference)
        self.data = {
            'name': 'Sponsor',
            'contact_name': self.user.get_full_name(),
            'contact_phone': '336-867-5309',
            'contact_address': '123 Main Street, Anytown, NC 90210',
            'external_url': 'https://example.com',
            'level': self.sponsor_level.pk,
            'wants_table': True,
            'wants_booth': True,
            'contact_emails-TOTAL_FORMS': '1',
            'contact_emails-INITIAL_FORMS': '1',
            'contact_emails-0-email': self.user.email,
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
        if response.status_code != 302:
            context = response.context
            print("form errors: {}".format(context['form'].errors))
            print("formset errors: {}".format(context['formset'].errors))
            print("formset nonfielderrors: {}".format(context['formset'].non_form_errors()))
            self.fail("Not 302, were there form errors?")
        self.assertRedirectsNoFollow(response, reverse('dashboard'))
        self.assertEqual(Sponsor.objects.count(), 1)

    def test_post_invalid(self):
        response = self.client.post(reverse(self.url_name), data={
            'contact_emails-TOTAL_FORMS': '0',
            'contact_emails-INITIAL_FORMS': '0',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(response.context['form'].is_bound)
        self.assertFalse(response.context['form'].is_valid())


class TestSponsorDetail(ViewTestMixin, TestCase):
    url_name = 'sponsor_detail'

    def setUp(self):
        super(TestSponsorDetail, self).setUp()
        self.user = UserFactory()
        self.login_user(self.user)
        self.sponsor = SponsorFactory(
            applicant=self.user,
            contact_name=self.user.get_full_name(),
            wants_table=True,
            wants_booth=True,
            active=True,
        )
        ContactEmail.objects.create(
            email=self.user.email,
            sponsor=self.sponsor,
        )
        self.mgmt_data = {
            'benefits-TOTAL_FORMS': '0',
            'benefits-INITIAL_FORMS': '8',
            'contact_emails-TOTAL_FORMS': '0',
            'contact_emails-INITIAL_FORMS': '1',
        }
        self.data = {
            'name': self.sponsor.name,
            'contact_name': self.user.get_full_name(),
            'contact_phone': self.sponsor.contact_phone,
            'contact_address': self.sponsor.contact_address,
            'external_url': self.sponsor.external_url,
            'level': self.sponsor.level.pk,
            'wants_table': self.sponsor.wants_table,
            'wants_booth': self.sponsor.wants_booth,
            'contact_emails-TOTAL_FORMS': '1',
            'contact_emails-INITIAL_FORMS': '1',
            'contact_emails-0-email': self.user.email,
            'benefits-TOTAL_FORMS': '0',
            'benefits-INITIAL_FORMS': '8',
        }
        # To add the benefits fields - punt
        formset = SponsorBenefitsFormSet(
            instance=self.sponsor,
            prefix="benefits",
            queryset=SponsorBenefit.objects.filter(active=True),
        )
        for form in formset.forms:
            for field in formset.fields:
                self.data[field.name_for_html] = field.value
        self.data['benefits-TOTAL_FORMS'] = len(formset.forms)


    def test_get_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse(self.url_name, args=[self.sponsor.pk]))
        self.assertEqual(response.status_code, 302)

    def test_post_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse(self.url_name, args=[self.sponsor.pk]), data=self.data)
        self.assertRedirectsToLogin(response)

    def test_get(self):
        response = self.client.get(reverse(self.url_name, args=[self.sponsor.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertFalse(response.context['form'].is_bound)

    def test_post_valid(self):
        response = self.client.post(reverse(self.url_name, args=[self.sponsor.pk]), data=self.data)
        if response.status_code == 200:
            form = response.context['form']
            self.assertTrue(form.is_valid(), msg=form.errors)
            print(response.content.decode('utf-8'))
        self.assertRedirectsNoFollow(response, reverse('dashboard'))
        self.assertEqual(Sponsor.objects.count(), 1)

    def test_post_invalid(self):
        response = self.client.post(reverse(self.url_name, args=[self.sponsor.pk]), data=self.mgmt_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(response.context['form'].is_bound)
        self.assertFalse(response.context['form'].is_valid())

    def test_add_contact_email(self):
        self.data['contact_emails-TOTAL_FORMS'] = '2'
        self.data['contact_emails-1-email'] = 'new@example.com'
        response = self.client.post(reverse(self.url_name, args=[self.sponsor.pk]), data=self.data)
        self.assertRedirectsNoFollow(response, reverse('dashboard'))
        sponsor = Sponsor.objects.get(pk=self.sponsor.pk)
        self.assertEqual(2, len(sponsor.contact_email_addrs()))
        self.assertIn('new@example.com', sponsor.contact_email_addrs())

    def test_add_contact_emails(self):
        self.data['contact_emails-TOTAL_FORMS'] = '3'
        self.data['contact_emails-1-email'] = 'new@example.com'
        self.data['contact_emails-2-email'] = 'newer@example.com'
        response = self.client.post(reverse(self.url_name, args=[self.sponsor.pk]), data=self.data)
        self.assertRedirectsNoFollow(response, reverse('dashboard'))
        sponsor = Sponsor.objects.get(pk=self.sponsor.pk)
        self.assertEqual(3, len(sponsor.contact_email_addrs()))

    def test_add_duplicate_contact_emails(self):
        self.assertEqual(1, ContactEmail.objects.filter(sponsor=self.sponsor).count())
        self.data['contact_emails-TOTAL_FORMS'] = '2'
        # This is the same as the existing one, except for case; we should
        # not allow adding it
        self.data['contact_emails-1-email'] = self.user.email.upper()
        response = self.client.post(reverse(self.url_name, args=[self.sponsor.pk]), data=self.data)
        # We get 200 instead of redirect if the form was rejected
        self.assertEqual(OK, response.status_code)
        self.assertFalse(response.context['email_formset'].is_valid())
        self.assertEqual(1, ContactEmail.objects.filter(sponsor=self.sponsor).count())

    def test_remove_contact_email(self):
        self.assertEqual(1, ContactEmail.objects.filter(sponsor=self.sponsor).count())
        self.sponsor.contact_emails.create(email="new@example.com")
        self.assertEqual(2, ContactEmail.objects.filter(sponsor=self.sponsor).count())
        self.data['contact_emails-TOTAL_FORMS'] = '2'
        self.data['contact_emails-1-email'] = 'new@example.com'
        self.data['contact_emails-1-DELETE'] = 'on'
        response = self.client.post(reverse(self.url_name, args=[self.sponsor.pk]), data=self.data)
        self.assertRedirectsNoFollow(response, reverse('dashboard'))
        self.assertEqual(1, ContactEmail.objects.filter(sponsor=self.sponsor).count())
