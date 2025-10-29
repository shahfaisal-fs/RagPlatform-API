from pydantic import BaseModel

class RAGConfig(BaseModel):
    document_processor: str = "unstructured"
    chunker: str = "markdown"
    embedder: str = "openai"
    vector_store: str = "chroma"
    pii_detector: str = "pressideo"
    governance: str = "basic"
    reranker: str = "none"  # none | cosine | llm