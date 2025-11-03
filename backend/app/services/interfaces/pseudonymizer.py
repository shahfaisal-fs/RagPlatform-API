from typing import List, Dict, Any, Tuple
from abc import ABC, abstractmethod

class Pseudonymizer(ABC):
    @abstractmethod
    async def tokenize(self, text: str, entities: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
        ...

    @abstractmethod
    async def encrypt(self, value: str) -> str:
        ...
