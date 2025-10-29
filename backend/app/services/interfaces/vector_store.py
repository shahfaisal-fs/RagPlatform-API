from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStore(ABC):
    @abstractmethod
    async def store(self, vectors: List[List[float]], texts: List[str], metadata: List[Dict[str, Any]]) -> None:
        """Store vectors and associated data."""
        ...
    
    @abstractmethod
    async def search(self, query_vector: List[float], top_k: int) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        ...
    
    @abstractmethod
    async def delete(self, ids: List[str]) -> None:
        """Delete vectors by ID."""
        ...