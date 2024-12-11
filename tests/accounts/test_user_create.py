from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.test import TestCase

from maistorbox.accounts.models import BaseUserModel, ContractorUserModel


class ContractorUserModelTest(TestCase):

    def setUp(self):
        self.base_user = BaseUserModel.objects.create(
            username="contractor1",
            email="contractor1@example.com",
            password=make_password('password123'),
        )

        self.contractor_user = ContractorUserModel.objects.create(
            user=self.base_user,
            phone_number="1234567890",
            profile_image='test_profile_image.png'
        )

    def test_base_user_creation(self):
        # Test BaseUserModel create
        self.assertEqual(self.base_user.username, "contractor1")
        self.assertEqual(self.base_user.email, "contractor1@example.com")
        self.assertTrue(self.base_user.check_password('password123'))

    def test_contractor_user_creation(self):
        # Test ContractorUserModel create
        self.assertEqual(self.contractor_user.user.username, "contractor1")
        self.assertEqual(self.contractor_user.phone_number, "1234567890")