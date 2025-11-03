import re
from typing import List, Dict, Any
from app.services.interfaces.pii_detector import PIIDetector

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?:\+\d{1,3}[-.\s]?)?(?:\d{2,4}[-.\s]?){2,4}\d{2,4}")

class RegexPIIDetector(PIIDetector):
    async def detect_pii(self, text: str) -> List[Dict[str, Any]]:
        entities: List[Dict[str, Any]] = []
        for m in EMAIL.finditer(text):
            entities.append({"type":"email","value":m.group(),"start":m.start(),"end":m.end()})
        for m in PHONE.finditer(text):
            entities.append({"type":"phone","value":m.group(),"start":m.start(),"end":m.end()})
        # (Optional) add NAME heuristics if needed later
        return entities
