from abc import ABC, abstractmethod
from typing import List

class EmbeddingStrategy(ABC):
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Convert text to embedding vector."""
        ...
    
    @abstractmethod
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Convert multiple texts to embedding vectors."""
        ...