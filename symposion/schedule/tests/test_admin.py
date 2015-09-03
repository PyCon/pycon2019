from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail
from django.forms.models import model_to_dict

from . import factories
from .. import admin


class TestPresentationAdmin(TestCase):
    def setUp(self):
        super(TestPresentationAdmin, self).setUp()
        self.pres_1 = factories.PresentationFactory()
        self.pres_2 = factories.PresentationFactory()
        self.pres_1_admin = admin.PresentationAdmin(
            self.pres_1,
            model_to_dict(self.pres_1))
        self.pres_2_admin = admin.PresentationAdmin(
            self.pres_2,
            model_to_dict(self.pres_2))
        self.form_1 = self.pres_1_admin.form
        self.form_2 = self.pres_2_admin.form

        self.app_label = self.pres_1._meta.app_label
        self.model_name = self.pres_1._meta.model_name

    def test_send_email_one_presentation_update(self):
        """An email should be sent when a presentation is updated by admin."""
        # Set up the request
        url_1 = reverse(
            "admin:{}_{}_change".format(self.app_label, self.model_name),
            args=[self.pres_1.pk])
        request_1 = self.client.post(url_1).wsgi_request

        # Make the update on pres_1
        self.pres_1_admin.save_model(
            request_1,
            self.pres_1,
            self.form_1,
            change=True)
        len_mailbox_after_send = len(mail.outbox)

        # Assertions
        self.assertEqual(1, len_mailbox_after_send)
        self.assertTrue(self.pres_1.title in mail.outbox[0].subject)
        self.assertTrue(self.pres_1.title in mail.outbox[0].body)

    def test_send_email_multiple_presentation_updates(self):
        """An email should be sent every time a presentation is updated by admin."""
        # Set up the request
        url_1 = reverse(
            "admin:{}_{}_change".format(self.app_label, self.model_name),
            args=[self.pres_1.pk])
        request_1 = self.client.post(url_1).wsgi_request
        url_2 = reverse(
            "admin:{}_{}_change".format(self.app_label, self.model_name),
            args=[self.pres_1.pk])
        request_2 = self.client.post(url_2).wsgi_request

        pres_1_updates = 1
        pres_2_updates = 3
        # Make the update for the number of times given in pres_1_updates
        for i in range(0, pres_1_updates):
            self.pres_1_admin.save_model(
                request_1,
                self.pres_1,
                self.form_1,
                change=True)
        # Make the update for the number of times given in pres_2_updates
        for i in range(0, pres_2_updates):
            self.pres_2_admin.save_model(
                request_2,
                self.pres_2,
                self.form_2,
                change=True)
        len_mailbox_after_send = len(mail.outbox)

        self.assertEqual(
            pres_1_updates + pres_2_updates,
            len_mailbox_after_send)
        # Assert for each update of pres_1
        for i in range(0, pres_1_updates):
            self.assertTrue(self.pres_1.title in mail.outbox[i].subject)
            self.assertTrue(self.pres_1.title in mail.outbox[i].body)
        # Assert for each update of pres_2
        for i in range(pres_1_updates, pres_2_updates + 1):
            self.assertTrue(self.pres_2.title in mail.outbox[i].subject)
            self.assertTrue(self.pres_2.title in mail.outbox[i].body)
