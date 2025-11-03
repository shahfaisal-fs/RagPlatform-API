from abc import ABC, abstractmethod
from typing import List

class LLMService(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str: ...
