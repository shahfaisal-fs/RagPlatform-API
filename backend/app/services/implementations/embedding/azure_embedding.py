import os, httpx
from typing import List
from app.services.interfaces.embedding_strategy import EmbeddingStrategy

AOAI = os.environ["AZ_OPENAI_ENDPOINT"].rstrip("/")
KEY  = os.environ["AZ_OPENAI_API_KEY"]
DEP  = os.environ["AZ_OPENAI_EMBEDDING_DEPLOYMENT"]
APIV = "2024-02-15-preview"

class AzureEmbedding(EmbeddingStrategy):
    async def embed_text(self, text: str) -> List[float]:
        return (await self.embed_texts([text]))[0]
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        url = f"{AOAI}/openai/deployments/{DEP}/embeddings?api-version={APIV}"
        headers = {"api-key": KEY, "Content-Type":"application/json"}
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(url, headers=headers, json={"input": texts})
            r.raise_for_status()
            data = r.json()
            return [d["embedding"] for d in data["data"]]
