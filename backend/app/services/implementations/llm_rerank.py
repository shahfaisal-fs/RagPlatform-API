from typing import List, Dict, Any
from app.services.interfaces.rerank_strategy import RerankStrategy

class LLMReranker(RerankStrategy):
    async def rerank(self, query_vector: List[float], docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Placeholder for future reranking using LLM relevance judgements
        return docs