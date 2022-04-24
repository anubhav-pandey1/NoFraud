from typing import Any

from core.models import Transaction, User


class FraudDetection:
    """Detects if a given transaction is fraudulent"""

    def __call__(self, data: dict, *args: Any, **kwds: Any) -> bool:
        self.data = data
        return True
