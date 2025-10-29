from typing import List, Dict, Any
from app.services.interfaces.service_interfaces import EmbeddingStrategy
from openai import OpenAI
import numpy as np

class OpenAIEmbeddingStrategy(EmbeddingStrategy):
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.client = OpenAI()
        self.model = model

    async def embed_text(self, text: str) -> List[float]:
        """Generate embeddings using OpenAI's API"""
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []