from rest_framework import serializers

from core.models import User, Transaction
from core.services import constants


class UserSerializer(serializers.ModelSerializer):
    """Used to create serialized User object"""

    class Meta:
        model = User


class TransactionSerializer(serializers.ModelSerializer):
    """Used to create serialized Transaction object"""

    sender = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=User.objects.all()
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "timestamp",
            "amount",
            "sender",
            "receiver_upi_id",
            "receiver_account_number",
        ]

    def validate(self, data):
        """Validation that exactly one of UPI ID and account number is provided."""
        receiver_upi_id = data.get("receiver_upi_id")
        receiver_account_number = data.get("receiver_account_number")
        if (receiver_upi_id and receiver_account_number) or (
            not receiver_upi_id and not receiver_account_number
        ):
            raise serializers.ValidationError(
                "Exactly one receiver payment detail (UPI ID or account no.) required."
            )
        return data
