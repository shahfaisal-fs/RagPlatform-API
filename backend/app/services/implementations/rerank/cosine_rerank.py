from typing import List, Dict, Any
import numpy as np
from app.services.interfaces.rerank_strategy import RerankStrategy

class CosineRerank(RerankStrategy):
    async def rerank(self, query_vector: List[float], docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Azure Search already returns by vector similarity; keep passthrough
        # Placeholder: compute re-similarity if docs contained embeddings.
        return docs
