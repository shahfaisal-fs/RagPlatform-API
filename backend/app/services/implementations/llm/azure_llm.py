import os, httpx
from app.services.interfaces.llm_service import LLMService

AOAI = os.environ["AZ_OPENAI_ENDPOINT"].rstrip("/")
KEY  = os.environ["AZ_OPENAI_API_KEY"]
DEP  = os.environ["AZ_OPENAI_CHAT_DEPLOYMENT"]
APIV = "2024-02-15-preview"

class AzureLLM(LLMService):
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        url = f"{AOAI}/openai/deployments/{DEP}/chat/completions?api-version={APIV}"
        headers = {"api-key": KEY, "Content-Type": "application/json"}
        payload = {"messages":[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}], "temperature":0.2}
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
