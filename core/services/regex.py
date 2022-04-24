def indian_upi() -> str:
    """Must have @, 2 chars before @ and 2 chars after @"""
    return "^[\w\.\-_]{2,}@[a-zA-Z]{2,}"


def indian_bank_account() -> str:
    """According to RBI, must have between 9 to 18 digits"""
    return "^\d{9,18}$"


def indian_mobile_number() -> str:
    """10 digit numbers that have the first digit b/w 6 to 9"""
    return "^[6-9]\d{9}$"
