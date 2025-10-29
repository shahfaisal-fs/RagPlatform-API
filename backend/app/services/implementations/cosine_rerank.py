from typing import List, Dict, Any
from math import sqrt
from app.services.interfaces.rerank_strategy import RerankStrategy

def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a)) or 1
    nb = sqrt(sum(x * x for x in b)) or 1
    return dot / (na * nb)

class CosineReranker(RerankStrategy):
    async def rerank(self, query_vector: List[float], docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        scored = [(cosine(query_vector, d.get("vector", [])), d) for d in docs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored]