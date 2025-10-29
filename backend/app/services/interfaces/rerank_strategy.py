from abc import ABC, abstractmethod
from typing import List, Dict, Any

class RerankStrategy(ABC):
    @abstractmethod
    async def rerank(self, query_vector: List[float], docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return documents sorted by relevance."""
        ...