import uuid

from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from core.validators import (
    indian_mobile_number_validators,
    indian_upi_id_validators,
    indian_bank_account_validators,
    transaction_amount_validators,
)
from core.choices import TransactionStatusChoices

# Create your models here.


class User(models.Model):

    phone_number = models.CharField(
        primary_key=True,
        unique=True,
        validators=indian_mobile_number_validators(),
    )

    upi_id = models.CharField(
        unique=True,
        null=True,
        blank=True,
        validators=indian_upi_id_validators(),
    )
    account_number = models.CharField(
        unique=True,
        null=True,
        blank=True,
        validators=indian_bank_account_validators(),
    )

    class Meta:
        """At least one field out of UPI ID or account number needs to be present"""

        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_upi_id_and_or_account_number",
                check=(~models.Q(upi_id__isnull=True, account_number__isnull=True)),
            )
        ]

    def __str__(self) -> str:
        return self.phone_number


class Transaction(models.Model):

    # Auto-generated fields
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, unique=True)
    timestamp = models.DateTimeField(default=timezone.now())
    # Fields to be provided
    amount = models.DecimalField(
        decimal_places=10, validators=transaction_amount_validators()
    )
    status = models.CharField(choices=TransactionStatusChoices.LIST)
    sender = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="transactions"
    )

    receiver_upi_id = models.CharField(
        null=True,
        blank=True,
        validators=indian_upi_id_validators(),
    )
    receiver_account_number = models.CharField(
        null=True,
        blank=True,
        validators=indian_bank_account_validators(),
    )

    class Meta:
        """Exactly one field out of UPI ID or account number needs to be present"""

        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_receiver_upi_id_or_receiver_account_number",
                check=(
                    models.Q(
                        receiver_upi_id__isnull=True,
                        receiver_account_number__isnull=False,
                    )
                    | models.Q(
                        receiver_upi_id__isnull=False,
                        receiver_account_number__isnull=True,
                    )
                ),
            )
        ]

    def __str__(self) -> str:
        amt = self.amount
        sender = self.sender
        receiver = (
            self.receiver_upi_id
            if self.receiver_upi_id
            else self.receiver_account_number
        )
        return f"INR {amt} : {sender} to {receiver}"
