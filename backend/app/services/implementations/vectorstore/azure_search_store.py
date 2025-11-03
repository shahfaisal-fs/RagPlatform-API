import os, httpx, logging, traceback
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ENDPOINT = os.environ["AZ_SEARCH_ENDPOINT"].rstrip("/")
KEY      = os.environ["AZ_SEARCH_API_KEY"]
INDEX    = os.environ["AZ_SEARCH_INDEX"]
API_V    = "2023-11-01"

class AzureAISearchStore:
    
    async def add_embeddings(self, texts: List[str], embeddings: List[List[float]], metadataDict: List[Dict[str, Any]]) -> None:
        url = f"{ENDPOINT}/indexes/{INDEX}/docs/index?api-version={API_V}"       
        value = []
        for i, (text, emb) in enumerate(zip(texts, embeddings)):
            metadata = metadataDict[i]
            doc = {
                "@search.action": "upload",
                "id": metadata["id"],
                "content": text[:8000],  # Limit length for stability
                "source": metadata["source"],
                "tenant": metadata["tenant"],
                "department": metadata["department"],
                "project_id": metadata["project_id"],
                "classification": metadata["classification"],
                "owner_user_id": metadata["owner_user_id"],
                "group_ids": metadata["group_ids"],
                "visibility": metadata["visibility"],
                "content_vector": emb,
                "content_vector_metadata": ""
            }
            value.append(doc)
        logger.info(f"🚀 Uploading {len(value)} embeddings to Azure Search index '{INDEX}' and the vlue is {value}")
        body = {"value": value}

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                resp = await client.post(
                    url, 
                    headers={"api-key": KEY, "Content-Type": "application/json"}, 
                    json=body
                )
                if resp.status_code >= 400:
                    logger.error(f"Azure Search add_embeddings failed: {resp.text}")
                    raise Exception(f"Azure Search error: {resp.status_code} {resp.text}")

                logger.info(f"✅ Azure Search: {len(value)} chunks uploaded")
        
        except Exception as e:
            logger.error(f"❌ ERROR uploading embeddings: {str(e)}")
            logger.debug(f"Trace: {traceback.format_exc()}")
            raise e

    
    async def search(self, query_embedding: List[float], top_k: int, filter_expr: str | None) -> List[Dict[str, Any]]:
        url = f"{ENDPOINT}/indexes/{INDEX}/docs/search?api-version={API_V}"

        body = {
            "vectorQueries": [
                {
                    "kind": "vector",
                    "vector": query_embedding,
                    "fields": "content_vector",
                    "k": top_k
                }
            ],
            "select": "id,content,source,tenant,department,project_id"
        }
        if filter_expr:
            body["filter"] = filter_expr

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                resp = await client.post(
                    url,
                    headers={"api-key": KEY, "Content-Type": "application/json"},
                    json=body
                )
                if resp.status_code >= 400:
                    logger.error(f"❌ Azure Search vector search failed: {resp.text}")
                    raise Exception(f"Azure Search search error: {resp.status_code} {resp.text}")

                data = resp.json()
                hits = []
                for v in data.get("value", []):
                    doc = v.get("document") or v  # ✅ handle both response formats
                    doc["score"] = v.get("@search.score", 0)  # ✅ attach score for ranking later
                    hits.append(doc)
                logger.info(f"🔍 Retrieved {len(hits)} search hits")
                return hits

        except Exception as e:
            logger.error(f"❌ SEARCH ERROR: {str(e)}")
            logger.debug(f"Trace: {traceback.format_exc()}")
            return []  # Return empty (but API will show no results)
