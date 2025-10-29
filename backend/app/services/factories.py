from typing import Dict, Any

from app.services.implementations.document_processor import UnstructuredDocumentProcessor
from app.services.implementations.chunk_strategy import RecursiveChunkStrategy
from app.services.implementations.embedding_strategy import OpenAIEmbeddingStrategy
from app.services.implementations.vector_store import ChromaVectorStore
from app.services.implementations.pii_detector import RegexPIIDetector
from app.services.implementations.data_governance import BasicDataGovernance
from app.services.implementations.none_rerank import NoReranker
from app.services.implementations.cosine_rerank import CosineReranker
from app.services.implementations.llm_rerank import LLMReranker

def get_document_processor(cfg: Dict[str, Any]):
    name = (cfg.get("document_processor") or "unstructured").lower()
    return {
        "unstructured": UnstructuredDocumentProcessor()
    }.get(name, UnstructuredDocumentProcessor())

def get_chunker(cfg: Dict[str, Any]):
    name = (cfg.get("chunker") or "recursive").lower()
    return {
        "recursive": RecursiveChunkStrategy()
    }.get(name, RecursiveChunkStrategy())

def get_embedder(cfg: Dict[str, Any]):
    name = (cfg.get("embedder") or "openai").lower()
    return {
        "openai": OpenAIEmbeddingStrategy()
    }.get(name, OpenAIEmbeddingStrategy())

def get_vector_store(cfg: Dict[str, Any]):
    name = (cfg.get("vector_store") or "chroma").lower()
    return {
        "chroma": ChromaVectorStore()
    }.get(name, ChromaVectorStore())

def get_pii_detector(cfg: Dict[str, Any]):
    name = (cfg.get("pii_detector") or "regex").lower()
    return {
        "regex": RegexPIIDetector()
    }.get(name, RegexPIIDetector())

def get_governance(cfg: Dict[str, Any]):
    name = (cfg.get("governance") or "basic").lower()
    return {
        "basic": BasicDataGovernance()
    }.get(name, BasicDataGovernance())

def get_reranker(cfg: Dict[str, Any]):
    name = (cfg.get("reranker") or "none").lower()
    return {
        "none": NoReranker(),
        "cosine": CosineReranker(),
        "llm": LLMReranker()
    }.get(name, NoReranker())