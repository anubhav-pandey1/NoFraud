from decimal import Decimal


def num_digits_in_decimal(n: "Decimal"):
    digits = Decimal(1)
    if n > 0:
        digits = n.log10() + Decimal(1)
    return digits
