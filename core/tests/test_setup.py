import random

from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from core.models import User, Transaction
from core.views import AttemptTransactionView


class TestSetupGeneral(APITestCase):
    """Test setup with general data"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.factory = APIRequestFactory()
        cls.transaction_view = AttemptTransactionView.as_view()
        cls.transaction_url = reverse("check-fraud")

        # User data setup
        cls.test_phone_num_1 = str(random.randint(6000000000, 9999999999))
        cls.test_account_num_1 = str(random.randint(100000000, 999999999999))
        cls.test_upi_id_1 = "abcdef@abcdef"
        cls.test_user_1 = User.objects.create(
            phone_number=cls.test_phone_num_1,
            upi_id=cls.test_upi_id_1,
            account_number=cls.test_account_num_1,
        )

        cls.test_phone_num_2 = str(random.randint(6000000000, 9999999999))
        cls.test_account_num_2 = str(random.randint(100000000, 999999999999))
        cls.test_user_2 = User.objects.create(
            phone_number=cls.test_phone_num_2,
            account_number=cls.test_account_num_2,
        )

        cls.test_phone_num_3 = str(random.randint(6000000000, 9999999999))
        cls.test_upi_id_3 = "wfwewef@gwoigjwi"
        cls.test_user_3 = User.objects.create(
            phone_number=cls.test_phone_num_3,
            upi_id=cls.test_upi_id_3,
        )


class TestSetupPositiveTransaction(TestSetupGeneral):
    """Test setup with positive transaction test cases data"""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        # Positive Transaction data
        cls.upi_transaction = {
            "sender": cls.test_phone_num_1,
            "amount": 1234.56,
            "receiver_upi_id": cls.test_upi_id_3,
        }

        cls.account_transaction = {
            "sender": cls.test_phone_num_2,
            "amount": 4234.56,
            "receiver_account_number": cls.test_account_num_1,
        }


class TestSetupNegativeTransaction(TestSetupGeneral):
    """Test setup with negative transaction test cases data"""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        # Negative Transaction data
        cls.non_existent_sender = {
            "sender": str(random.randint(6000000000, 9999999999)),
            "amount": 1234.56,
            "receiver_upi_id": cls.test_upi_id_1,
        }

        cls.invalid_sender = {
            "sender": "abcf3if3",
            "amount": 1234.56,
            "receiver_upi_id": cls.test_upi_id_1,
        }

        cls.extra_receiver_details = {
            "sender": cls.test_phone_num_1,
            "amount": 1234.56,
            "receiver_upi_id": cls.test_upi_id_1,
            "receiver_account_number": str(random.randint(100000000, 999999999999)),
        }


class TestSetupFraudulentTransaction(TestSetupPositiveTransaction):
    """Test setup with fraudulent transaction test cases data"""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        # Fraudulent Transaction data
        cls.self_sender_account = {
            "sender": cls.test_phone_num_1,
            "amount": 4234.56,
            "receiver_account_number": cls.test_account_num_1,
        }

        cls.self_sender_upi = {
            "sender": cls.test_phone_num_1,
            "amount": 4234.56,
            "receiver_upi_id": cls.test_upi_id_1,
        }
