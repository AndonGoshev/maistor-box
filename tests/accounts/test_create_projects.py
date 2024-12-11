from django.test import TestCase
from maistorbox.accounts.models import BaseUserModel, ContractorUserModel, ContractorProjectModel
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError


class ContractorProjectModelTest(TestCase):

    def setUp(self):
        # Create regular user
        self.base_user = BaseUserModel.objects.create(
            username="contractor1",
            email="contractor1@example.com",
            password=make_password('password123'),
        )

        # Create contractor user linked to base user
        self.contractor_user = ContractorUserModel.objects.create(
            user=self.base_user,
            phone_number="1234567890",
            profile_image='test_profile_image.png'
        )

    def test_project_creation(self):
        # Test valid project creation
        project = ContractorProjectModel.objects.create(
            project_name="Test Project",
            project_description="Description of the test project",
            average_price_for_similar_project=500.00,
            contractor_user=self.contractor_user
        )
        self.assertEqual(project.project_name, "Test Project")
        self.assertEqual(project.project_description, "Description of the test project")
        self.assertEqual(project.average_price_for_similar_project, 500.00)
        self.assertEqual(project.contractor_user, self.contractor_user)


    def test_empty_project_description(self):
        # Test empty project_description (should fail)
        project = ContractorProjectModel(
            project_name="Valid Project Name",
            project_description="",
            contractor_user=self.contractor_user
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_invalid_average_price(self):
        # Test invalid average_price_for_similar_project (should fail with negative price)
        project = ContractorProjectModel(
            project_name="Test Project",
            project_description="Description of the test project",
            average_price_for_similar_project=-100.00,
            contractor_user=self.contractor_user
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_project_belongs_to_contractor(self):
        # Test if project is linked to contractor
        project = ContractorProjectModel.objects.create(
            project_name="Project for Contractor",
            project_description="This project should belong to the contractor",
            contractor_user=self.contractor_user
        )
        self.assertEqual(project.contractor_user, self.contractor_user)
        self.assertIn(project, self.contractor_user.projects.all())  # Check if project is associated with contractor
