from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStore(ABC):
    @abstractmethod
    async def add_embeddings(self, texts: List[str], embeddings: List[List[float]], metadata: List[Dict[str, Any]]) -> None: ...
    @abstractmethod
    async def search(self, query_embedding: List[float], top_k: int, filter_expr: str | None) -> List[Dict[str, Any]]: ...
