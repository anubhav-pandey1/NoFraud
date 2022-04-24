from django.core.validators import (
    BaseValidator,
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
)

from core.services import regex, constants


def indian_mobile_number_validators() -> "list[BaseValidator]":
    return [RegexValidator(regex.indian_mobile_number())]


def indian_upi_id_validators() -> "list[BaseValidator]":
    return [RegexValidator(regex.indian_upi())]


def indian_bank_account_validators() -> "list[BaseValidator]":
    return [RegexValidator(regex.indian_bank_account())]


def transaction_amount_validators() -> "list[BaseValidator]":
    return [
        MinValueValidator(constants.MIN_TRANSACTION_AMOUNT),
        MaxValueValidator(constants.MAX_TRANSACTION_AMOUNT),
    ]
