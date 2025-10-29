from abc import ABC, abstractmethod
from typing import Dict, Any

class DataGovernance(ABC):
    @abstractmethod
    async def validate_document(self, content: str, metadata: Dict[str, Any]) -> bool:
        """Validate if document meets governance requirements."""
        ...