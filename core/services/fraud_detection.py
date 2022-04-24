from datetime import timedelta

from django.utils import timezone
from django.db.models import Q
from django.db.models.query import QuerySet

from core.models import Transaction, User
from core.choices import TransactionStatusChoices


class FraudDetection:
    """Detects if a given transaction is fraudulent"""

    FRAUD_WINDOW_MINUTES = 2
    SAME_USER_LIMIT = 10
    ALL_USER_LIMIT = 30
    FRAUD_COOLDOWN_DAYS = 30
    FRAUD_MONTHLY_LIMIT = 1

    def __init__(self, data: dict) -> None:
        self.data = data
        self.sender_phone_number = self.data["sender"]
        self.sender = User.objects.filter(
            phone_number__exact=self.sender_phone_number
        ).first()
        self.amount = self.data["amount"]
        self.receiver_upi = self.data.get("receiver_upi_id")
        self.receiver_account = self.data.get("receiver_account_number")

    def __call__(self) -> bool:
        return (
            self.send_to_self()
            or self.rapid_same_transactions()
            or self.fraud_cooldown_check()
        )

    def send_to_self(self) -> bool:
        """Check if senders send payment to their own UPI ID or bank account"""
        if self.sender.upi_id and self.sender.upi_id == self.receiver_upi:
            return True
        elif (
            self.sender.account_number
            and self.sender.account_number == self.receiver_account
        ):
            return True
        return False

    def rapid_same_transactions(self) -> bool:
        """Check if same value transactions are occuring rapidly"""

        time_range = timezone.now() + timedelta(
            minutes=-FraudDetection.FRAUD_WINDOW_MINUTES
        )
        latest_transactions = Transaction.objects.filter(timestamp__gte=time_range)
        return self._same_sender_check(latest_transactions) or self._all_senders_check(
            latest_transactions
        )

    def _same_sender_check(self, latest_transactions: QuerySet) -> bool:
        """Check if a sender is sending more than 10 transactions of same amount
        in the last 2 minutes"""
        suspicious_count = latest_transactions.filter(
            Q(amount__exact=self.amount)
            & Q(sender__phone_number__exact=self.sender_phone_number)
        ).count()
        return suspicious_count > FraudDetection.SAME_USER_LIMIT

    def _all_senders_check(self, latest_transactions: QuerySet) -> bool:
        """Check if any sender(s) are sending more than 30 transactions of same amount
        in the last 2 minutes"""
        suspicious_count = latest_transactions.filter(
            Q(amount__exact=self.amount)
        ).count()
        return suspicious_count > FraudDetection.ALL_USER_LIMIT

    def fraud_cooldown_check(self) -> bool:
        """If a user has more than 1 fraudulent transaction in a cool-down period of last 30 days,
        the current transaction will also be marked as fraudulent"""
        # self.sender.select_related()
        time_range = timezone.now() + timedelta(
            days=-FraudDetection.FRAUD_COOLDOWN_DAYS
        )
        fraud_count = Transaction.objects.filter(
            Q(sender__phone_number__exact=self.sender_phone_number)
            & Q(timestamp__gte=time_range)
            & Q(status__exact=TransactionStatusChoices.TERRORIST)
        ).count()
        return fraud_count > FraudDetection.FRAUD_MONTHLY_LIMIT
