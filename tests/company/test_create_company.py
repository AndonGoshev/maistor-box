from django.core.exceptions import ValidationError
from django.test import TestCase

from maistorbox.company.models import CompanyModel


class CompanyModelTest(TestCase):

    def test_invalid_creation_of_second_company(self):
        # Create the first company
        company1 = CompanyModel.objects.create(
            name="Company 1",
            phone_number="123456789",
            email="company1@example.com",
            address="123 Main St.",
            instagram_page_url="https://instagram.com/company1",
            facebook_page_url="https://facebook.com/company1",
            linkedin_page_url="https://linkedin.com/company1"
        )

        # Try to create a second company (should raise ValidationError)
        try:
            company2 = CompanyModel(
                name="Company 2",
                phone_number="987654321",
                email="company2@example.com",
                address="456 Elm St.",
                instagram_page_url="https://instagram.com/company2",
                facebook_page_url="https://facebook.com/company2",
                linkedin_page_url="https://linkedin.com/company2"
            )
            company2.full_clean()
            company2.save()  # This should raise the ValidationError in the `save` method
            self.fail("ValidationError not raised")
        except ValidationError:
            pass

    def test_valid_create_one_company(self):
        # Create the first company successfully
        company = CompanyModel.objects.create(
            name="Company 1",
            phone_number="123456789",
            email="company1@example.com",
            address="123 Main St.",
            instagram_page_url="https://instagram.com/company1",
            facebook_page_url="https://facebook.com/company1",
            linkedin_page_url="https://linkedin.com/company1"
        )

        # Assert the company is created successfully
        self.assertEqual(CompanyModel.objects.count(), 1)
        self.assertEqual(company.name, "Company 1")