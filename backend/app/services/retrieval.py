from typing import List, Dict, Any
from app.services.factories import get_embedder, get_vector_store, get_reranker

async def retrieve_relevant_chunks(query: str, top_k: int, cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Get services
    embedder = get_embedder(cfg)
    store = get_vector_store(cfg)
    
    # Get query vector
    qv = await embedder.embed_text(query)
    
    # Search and rerank
    raw_hits = store.search(qv, top_k)
    reranker = get_reranker(cfg)
    hits = await reranker.rerank(qv, raw_hits)
    
    return hits