from typing import List, Dict, Any
from app.services.interfaces.service_interfaces import VectorStore
import chromadb
from chromadb.config import Settings

class ChromaVectorStore(VectorStore):
    def __init__(self, collection_name: str = "documents"):
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name=collection_name)

    async def add_embeddings(self, texts: List[str], embeddings: List[List[float]], metadata: List[Dict[str, Any]]) -> List[str]:
        """Store embeddings in Chroma"""
        try:
            ids = [str(i) for i in range(len(texts))]
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadata,
                ids=ids
            )
            return ids
        except Exception as e:
            print(f"Error adding embeddings: {e}")
            return []

    async def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search similar embeddings in Chroma"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            return [
                {
                    "text": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception as e:
            print(f"Error searching embeddings: {e}")
            return []