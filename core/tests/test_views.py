from rest_framework import status

from core.tests.test_setup import (
    TestSetupPositiveTransaction,
    TestSetupNegativeTransaction,
    TestSetupFraudulentTransaction,
)
from core.services.fraud_detection import FraudDetection


class TransactionPositiveTests(TestSetupPositiveTransaction):
    """Tests for working scenarios of transactions"""

    def test_transaction_to_upi(self):
        transaction_request = self.factory.post(
            self.transaction_url, data=self.upi_transaction, format="json"
        )
        transaction_response = self.transaction_view(transaction_request)
        self.assertEqual(transaction_response.status_code, status.HTTP_202_ACCEPTED)

    def test_transaction_to_account_number(self):
        transaction_request = self.factory.post(
            self.transaction_url, data=self.account_transaction, format="json"
        )
        transaction_response = self.transaction_view(transaction_request)
        self.assertEqual(transaction_response.status_code, status.HTTP_202_ACCEPTED)


class TransactionNegativeTests(TestSetupNegativeTransaction):
    """Tests for failing (non-fraudulent) scenarios of transactions"""

    def test_non_existent_sender(self):
        transaction_request = self.factory.post(
            self.transaction_url, data=self.non_existent_sender, format="json"
        )
        transaction_response = self.transaction_view(transaction_request)
        self.assertEqual(transaction_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_sender(self):
        transaction_request = self.factory.post(
            self.transaction_url, data=self.invalid_sender, format="json"
        )
        transaction_response = self.transaction_view(transaction_request)
        self.assertEqual(transaction_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_extra_receiver_details(self):
        transaction_request = self.factory.post(
            self.transaction_url, data=self.extra_receiver_details, format="json"
        )
        transaction_response = self.transaction_view(transaction_request)
        self.assertEqual(transaction_response.status_code, status.HTTP_400_BAD_REQUEST)


class TransactionFraudulentTests(TestSetupFraudulentTransaction):
    """Tests for fraudulent scenarios of transactions"""

    def test_self_sender_account(self):
        transaction_request = self.factory.post(
            self.transaction_url, data=self.self_sender_account, format="json"
        )
        transaction_response = self.transaction_view(transaction_request)
        self.assertEqual(transaction_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_self_sender_upi(self):
        transaction_request = self.factory.post(
            self.transaction_url, data=self.self_sender_upi, format="json"
        )
        transaction_response = self.transaction_view(transaction_request)
        self.assertEqual(transaction_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rapid_same_transactions_same_user(self):
        limit = FraudDetection.SAME_USER_LIMIT
        for count in range(limit + 1):
            transaction_request = self.factory.post(
                self.transaction_url, data=self.upi_transaction, format="json"
            )
            transaction_response = self.transaction_view(transaction_request)
            expected_status = (
                status.HTTP_403_FORBIDDEN if count > limit else status.HTTP_202_ACCEPTED
            )
            self.assertEqual(transaction_response.status_code, expected_status)
