import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import FinancialAidApplication, FinancialAidMessage,\
    PYTHON_EXPERIENCE_BEGINNER, Receipt
from pycon.finaid.forms import FinancialAidApplicationForm, ReviewerMessageForm,\
    ReceiptForm


today = datetime.date.today()


class FinancialAidTest(TestCase):

    def test_form(self):
        user = User.objects.create_user("Foo")
        instance = FinancialAidApplication(user=user)
        form = FinancialAidApplicationForm(instance=instance)
        self.assertFalse(form.is_valid())
        data = dict(
            profession="Foo",
            experience_level=PYTHON_EXPERIENCE_BEGINNER,
            what_you_want="money",
            use_of_python="fun",
            presenting=1,
            amount_requested="0.00",
            travel_plans="get there",
        )
        instance = FinancialAidApplication(user=user)
        form = FinancialAidApplicationForm(data, instance=instance)
        self.assertTrue(form.is_valid(), msg=form.errors)

        # Leave out a required field
        del data['presenting']
        form = FinancialAidApplicationForm(data, instance=instance)
        self.assertFalse(form.is_valid())

    def test_reviewer_message_form(self):
        user = User.objects.create_user("Foo")
        application = FinancialAidApplication.objects.create(
            user=user,
            profession="Foo",
            experience_level=PYTHON_EXPERIENCE_BEGINNER,
            what_you_want="money",
            use_of_python="fun",
            presenting=1,
        )
        application.save()
        message = FinancialAidMessage(user=user, application=application)
        data = {
            'visible': False,
            'message': 'TestMessage'
        }
        form = ReviewerMessageForm(data, instance=message)
        self.assertTrue(form.is_valid())
        message = form.save()
        message = FinancialAidMessage.objects.get(pk=message.pk)
        self.assertFalse(message.visible)
        self.assertEqual("TestMessage", message.message)

        data['visible'] = True
        form = ReviewerMessageForm(data, instance=message)
        self.assertTrue(form.is_valid())
        message = form.save()
        message = FinancialAidMessage.objects.get(pk=message.pk)
        self.assertTrue(message.visible)


class TestReceiptForm(TestCase):

    def setUp(self):
        super(TestReceiptForm, self).setUp()
        self.user = User.objects.create_user("Foo")
        self.application = FinancialAidApplication.objects.create(
            user=self.user,
            profession="Foo",
            experience_level=PYTHON_EXPERIENCE_BEGINNER,
            what_you_want="money",
            use_of_python="fun",
            presenting=1,
        )
        self.application.save()

    def test_valid_receipt(self):
        """Checks form is valid with SimpleUploadeFile extension pdf or png."""
        simple_file_pdf = SimpleUploadedFile(
            'test_file.pdf',
            str('contents of the test file'))
        simple_file_png = SimpleUploadedFile(
            'test_file.png',
            str('contents of the test file'))
        receipt_pdf = Receipt(
            application=self.application,
            description='description',
            amount=1,
            receipt_image=simple_file_pdf)
        receipt_png = Receipt(
            application=self.application,
            description='description',
            amount=1,
            receipt_image=simple_file_png)
        receipt_pdf.user = self.user
        receipt_png.user = self.user
        receipt_pdf.save()
        receipt_png.save()
        data_pdf = {'description': 'description',
                    'amount': 1,
                    'receipt_image': simple_file_pdf}
        data_png = {'description': 'description',
                    'amount': 1,
                    'receipt_image': simple_file_png}
        form_pdf = ReceiptForm(data_pdf, instance=receipt_pdf)
        form_png = ReceiptForm(data_png, instance=receipt_png)

        self.assertTrue(form_pdf.is_valid())
        self.assertTrue(form_png.is_valid())

    def test_missing_image(self):
        """Verifies the form is not valid when the receipt_image field is blank."""
        receipt = Receipt(
            application=self.application,
            description='description',
            amount=1)
        receipt.user = self.user
        receipt.save()
        data = {'description': 'description',
                'amount': 1}
        form = ReceiptForm(data, instance=receipt)

        self.assertFalse(form.is_valid())
