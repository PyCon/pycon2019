import datetime
import StringIO

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files.base import ContentFile

from ..models import FinancialAidApplication, FinancialAidMessage,\
    PYTHON_EXPERIENCE_BEGINNER, Receipt
from pycon.finaid.forms import FinancialAidApplicationForm, ReviewerMessageForm,\
    ReceiptForm

from PIL import Image

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
        # Use StringIO to create files
        png_file = StringIO.StringIO('portable network graphics file')
        pdf_file = StringIO.StringIO('portable document format file')
        # Use PIL Image to create new png and pdf files
        Image.new('RGB', size=(50, 50), color=(256, 0, 0)).save(png_file, 'png')
        Image.new('RGB', size=(50, 50), color=(256, 0, 0)).save(pdf_file, 'pdf')
        png_file.seek(0)
        pdf_file.seek(0)
        # Django-friendly ContentFiles
        django_friendly_png_file = ContentFile(png_file.read(), 'test_file.png')
        django_friendly_pdf_file = ContentFile(pdf_file.read(), 'test_file.pdf')
        # Create receipts with these files in the receipt_image field
        receipt_png = Receipt(
            application=self.application,
            description='description png',
            amount=1,
            receipt_image=django_friendly_png_file)
        receipt_pdf = Receipt(
            application=self.application,
            description='description pdf',
            amount=1,
            receipt_image=django_friendly_pdf_file)
        receipt_png.user = self.user
        receipt_pdf.user = self.user
        # Save the receipts
        receipt_png.save()
        receipt_pdf.save()
        # Data for the form
        data_png = {'description': 'description png',
                    'amount': 1,
                    'receipt_image': django_friendly_png_file}
        data_pdf = {'description': 'description pdf',
                    'amount': 1,
                    'receipt_image': django_friendly_pdf_file}
        form_png = ReceiptForm(data_png, instance=receipt_png)
        form_pdf = ReceiptForm(data_pdf, instance=receipt_pdf)

        self.assertTrue(form_png.is_valid())
        self.assertTrue(form_pdf.is_valid())

    def test_missing_image(self):
        """Verifies the form is not valid when the receipt_image field is blank."""
        receipt = Receipt(
            application=self.application,
            description='description of file',
            amount=1)
        receipt.user = self.user
        receipt.save()
        data = {'description': 'description of file',
                'amount': 1}
        form = ReceiptForm(data, instance=receipt)

        self.assertFalse(form.is_valid())
