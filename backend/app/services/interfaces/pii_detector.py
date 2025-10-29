from abc import ABC, abstractmethod
from typing import Dict, Any, List

class PIIDetector(ABC):
    @abstractmethod
    async def detect_pii(self, text: str) -> List[Dict[str, Any]]:
        """Detect PII in text and return findings."""
        ...