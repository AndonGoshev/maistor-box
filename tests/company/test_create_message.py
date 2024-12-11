from django.test import TestCase
from django.core.exceptions import ValidationError

from maistorbox.company.models import CompanyModel, Message


class MessageModelTest(TestCase):

    def test_invalid_create_message_with_short_content(self):
        company = CompanyModel.objects.create(
            name="Company 1",
            phone_number="123456789",
            email="company1@example.com",
            address="123 Main St.",
            instagram_page_url="https://instagram.com/company1",
            facebook_page_url="https://facebook.com/company1",
            linkedin_page_url="https://linkedin.com/company1"
        )

        message = Message(
            company=company,
            sender_email="sender@example.com",
            content="Short"
        )

        with self.assertRaises(ValidationError):
            message.full_clean()

    def test_valid_create_message_with_valid_content(self):
        company = CompanyModel.objects.create(
            name="Company 1",
            phone_number="123456789",
            email="company1@example.com",
            address="123 Main St.",
            instagram_page_url="https://instagram.com/company1",
            facebook_page_url="https://facebook.com/company1",
            linkedin_page_url="https://linkedin.com/company1"
        )

        message = Message(
            company=company,
            sender_email="sender@example.com",
            content="This is valid content"
        )

        message.full_clean()
        message.save()

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.content, "This is valid content")