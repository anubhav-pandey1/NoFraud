from typing import Any

from core.models import Transaction, User


class FraudDetection:
    """Detects if a given transaction is fraudulent"""

    def __init__(self, data: dict) -> None:
        self.data = data

    def __call__(self, *args: Any, **kwds: Any) -> bool:
        return False
