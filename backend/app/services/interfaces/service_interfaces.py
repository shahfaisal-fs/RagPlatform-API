from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DocumentProcessor(ABC):
    @abstractmethod
    async def process_document(self, file_content: bytes, metadata: Dict[str, Any]) -> str:
        """Process a document and return its content"""
        pass

class ChunkStrategy(ABC):
    @abstractmethod
    async def chunk_text(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        """Split text into chunks with specified size and overlap"""
        pass

class EmbeddingStrategy(ABC):
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for the given text"""
        pass

class VectorStore(ABC):
    @abstractmethod
    async def add_embeddings(self, texts: List[str], embeddings: List[List[float]], metadata: List[Dict[str, Any]]) -> List[str]:
        """Store text embeddings with metadata"""
        pass

    @abstractmethod
    async def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar embeddings"""
        pass

class LLMService(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, context: List[str], temperature: float = 0.7) -> str:
        """Generate response using LLM"""
        pass

class PIIDetector(ABC):
    @abstractmethod
    async def detect_pii(self, text: str) -> Dict[str, List[str]]:
        """Detect PII in text"""
        pass

class DataGovernance(ABC):
    @abstractmethod
    async def validate_document(self, content: str, metadata: Dict[str, Any]) -> bool:
        """Validate document against governance rules"""
        pass

    @abstractmethod
    async def apply_retention_policy(self, document_id: str) -> bool:
        """Apply retention policy to document"""
        pass