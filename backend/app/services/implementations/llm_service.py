from typing import List, Dict, Any
from app.services.interfaces.service_interfaces import LLMService
from openai import OpenAI

class OpenAILLMService(LLMService):
    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.client = OpenAI()
        self.model = model

    async def generate_response(self, prompt: str, context: List[str], temperature: float = 0.7) -> str:
        """Generate response using OpenAI's API"""
        try:
            # Prepare context and prompt
            messages = [
                {"role": "system", "content": "You are a helpful assistant. Use the following context to answer questions."},
                {"role": "system", "content": f"Context:\n{' '.join(context)}"},
                {"role": "user", "content": prompt}
            ]

            # Generate response
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""