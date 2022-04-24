from django.core.validators import (
    BaseValidator,
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
)

from core.services import regex, constants


class Validators:
    INDIAN_MOBILE_NUMBERS = [
        RegexValidator(
            regex=regex.indian_mobile_number(),
            message="Please enter a valid Indian mobile number",
            code="invalid_phone_number",
        )
    ]

    INDIAN_UPI_ID = [
        RegexValidator(
            regex=regex.indian_upi(),
            message="Please enter a valid Indian UPI ID",
            code="invalid_upi_id",
        )
    ]

    INDIAN_BANK_ACCOUNT = [
        RegexValidator(
            regex=regex.indian_bank_account(),
            message="Please enter a valid Indian bank account number",
            code="invalid_account_number",
        )
    ]

    TRANSACTION_AMOUNT = [
        MinValueValidator(constants.MIN_TRANSACTION_AMOUNT),
        MaxValueValidator(constants.MAX_TRANSACTION_AMOUNT),
    ]
