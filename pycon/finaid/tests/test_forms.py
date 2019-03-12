import datetime
import StringIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

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
            presenting=1,
            amount_requested="0.00",
            travel_plans="get there",
            i_have_read=True,
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
            presenting=1,
        )
        self.application.save()

    def test_valid_receipt_png(self):
        """Checks form is valid with SimpleUploadeFile extension png."""
        # Use StringIO to create files
        png_file = StringIO.StringIO('portable network graphics file')
        # Use PIL Image to create new png and pdf files
        Image.new('RGB', size=(50, 50), color=(256, 0, 0)).save(png_file, 'png')
        png_file.seek(0)
        # Django-friendly ContentFiles
        file = SimpleUploadedFile('test_file.png', png_file.read())
        # Data for the form
        data_png = {'description': '',
                    'receipt_type': 'airfare',
                    'date': '2019-03-02',
                    'amount_0': 1,
                    'amount_1': 'USD',
                    }
        files = {'receipt_image': file}

        form_png = ReceiptForm(data_png, files, instance=Receipt(application=self.application))

        self.assertTrue(form_png.is_valid(), msg=form_png.errors)
        form_png.save()

    def test_valid_receipt_pdf(self):
        """Checks form is valid with SimpleUploadeFile extension pdf"""
        # Use StringIO to create files
        pdf_file = StringIO.StringIO('portable document format file')
        # Use PIL Image to create new png and pdf files
        Image.new('RGB', size=(50, 50), color=(256, 0, 0)).save(pdf_file, 'pdf')
        pdf_file.seek(0)
        file = SimpleUploadedFile('test_file.pdf', pdf_file.read())
        # Data for the form
        data_pdf = {'description': 'description pdf',
                    'receipt_type': 'airfare',
                    'date': '2019-03-02',
                    'amount_0': 1,
                    'amount_1': 'USD',
                    }
        files = {'receipt_image': file}
        form_pdf = ReceiptForm(data_pdf, files, instance=Receipt(application=self.application))

        self.assertTrue(form_pdf.is_valid(), msg=form_pdf.errors)
        form_pdf.save()

    def test_missing_image(self):
        """Verifies the form is not valid when the receipt_image field is blank."""
        data = {'description': 'description of file',
                'receipt_type': 'other',
                'date': '2019-03-02',
                'amount_0': 1,
                'amount_1': 'USD',
                }
        form = ReceiptForm(data, {}, instance=Receipt(application=self.application))

        self.assertIn('This field is required.', form.errors['receipt_image'])
