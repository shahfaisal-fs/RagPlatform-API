from typing import List, Dict, Any
from app.services.factories import get_embedder, get_vector_store, get_reranker
from app.services.retrieval import retrieve_relevant_chunks

async def get_chat_response(query: str, chat_history: List[Dict[str, Any]], cfg: Dict[str, Any]) -> str:
    # Get relevant chunks
    chunks = await retrieve_relevant_chunks(query, cfg.get("top_k", 3), cfg)
    
    # Build context from chunks
    context = "\n\n".join([c["text"] for c in chunks])
    
    # TODO: Add LLM response generation using context + chat history
    
    return "Placeholder response"