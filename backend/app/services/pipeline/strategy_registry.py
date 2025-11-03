from typing import Dict, Type
from app.services.interfaces.chunk_strategy import ChunkStrategy
from app.services.interfaces.embedding_strategy import EmbeddingStrategy
from app.services.interfaces.vector_store import VectorStore
from app.services.interfaces.rerank_strategy import RerankStrategy
from app.services.interfaces.pii_detector import PIIDetector
from app.services.interfaces.data_governance import DataGovernance
from app.services.interfaces.llm_service import LLMService
from app.services.interfaces.pseudonymizer import Pseudonymizer

# Implementations
from app.services.implementations.chunking.paragraph_chunker import ParagraphChunker
from app.services.implementations.chunking.recursive_chunker import RecursiveChunker
from app.services.implementations.chunking.semantic_chunker import SemanticChunker

from app.services.implementations.embedding.azure_embedding import AzureEmbedding
from app.services.implementations.vectorstore.azure_search_store import AzureAISearchStore
from app.services.implementations.rerank.cosine_rerank import CosineRerank
from app.services.implementations.pii.regex_detector import RegexPIIDetector

from app.services.implementations.pii.pseudonymizer import SimplePseudonymizer 
from app.services.implementations.governance.basic_governance import BasicGovernance
from app.services.implementations.llm.azure_llm import AzureLLM

class StrategyRegistry:
    chunkers: Dict[str, Type[ChunkStrategy]] = {
        "paragraph": ParagraphChunker,
        "recursive": RecursiveChunker,
        "semantic":  lambda: SemanticChunker(AzureEmbedding())
    }
    embedders: Dict[str, Type[EmbeddingStrategy]] = {
        "azure-openai": AzureEmbedding
    }
    stores: Dict[str, Type[VectorStore]] = {
        "azure-search": AzureAISearchStore
    }
    rerankers: Dict[str, Type[RerankStrategy]] = {
        "cosine": CosineRerank,
        "none": CosineRerank  # default to cosine light rerank
    }
    pii: Dict[str, Type[PIIDetector]] = {
        "regex": RegexPIIDetector
    }
    pseudonymizers: Dict[str, Type[Pseudonymizer]] = {    
        "simple": SimplePseudonymizer,
    }
    governance: Dict[str, Type[DataGovernance]] = {
        "basic": BasicGovernance
    }
    llms: Dict[str, Type[LLMService]] = {
        "azure-openai": AzureLLM
    }
