from abc import ABC, abstractmethod
from typing import List

class ChunkStrategy(ABC):
    @abstractmethod
    async def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        ...