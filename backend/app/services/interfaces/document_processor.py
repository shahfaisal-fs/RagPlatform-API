from abc import ABC, abstractmethod
from typing import Dict, Any

class DocumentProcessor(ABC):
    @abstractmethod
    async def process_document(self, file_content: bytes, metadata: Dict[str, Any]) -> str:
        """Process a document and return its text content."""
        ...