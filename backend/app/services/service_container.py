from typing import Dict, Type
from app.services.interfaces.service_interfaces import (
    DocumentProcessor, ChunkStrategy, EmbeddingStrategy,
    VectorStore, LLMService, PIIDetector, DataGovernance
)
from app.services.interfaces.rerank_strategy import RerankStrategy
from app.services.implementations.document_processor import UnstructuredDocumentProcessor
from app.services.implementations.chunk_strategy import RecursiveChunkStrategy
from app.services.implementations.embedding_strategy import OpenAIEmbeddingStrategy
from app.services.implementations.vector_store import ChromaVectorStore
from app.services.implementations.llm_service import OpenAILLMService
from app.services.implementations.pii_detector import RegexPIIDetector
from app.services.implementations.data_governance import BasicDataGovernance
from app.services.implementations.none_rerank import NoReranker
from app.services.implementations.cosine_rerank import CosineReranker
from app.services.implementations.llm_rerank import LLMReranker

class ServiceContainer:
    def __init__(self):
        self._services: Dict[Type, object] = {}
        self._initialize_services()

    def _initialize_services(self):
        # Initialize default implementations
        self._services[DocumentProcessor] = UnstructuredDocumentProcessor()
        self._services[ChunkStrategy] = RecursiveChunkStrategy()
        self._services[EmbeddingStrategy] = OpenAIEmbeddingStrategy()
        self._services[VectorStore] = ChromaVectorStore()
        self._services[LLMService] = OpenAILLMService()
        self._services[PIIDetector] = RegexPIIDetector()
        self._services[DataGovernance] = BasicDataGovernance()
        
        # Set default reranking strategy (NoReranker)
        self._services[RerankStrategy] = NoReranker()

    def get_service(self, service_type: Type) -> object:
        """Get service implementation by type"""
        return self._services.get(service_type)

    def register_service(self, service_type: Type, implementation: object):
        """Register a new service implementation"""
        self._services[service_type] = implementation

# Create global service container instance
service_container = ServiceContainer()