from typing import List, Dict, Any
from app.services.interfaces.service_interfaces import PIIDetector
import re

class RegexPIIDetector(PIIDetector):
    def __init__(self):
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }

    async def detect_pii(self, text: str) -> Dict[str, List[str]]:
        """Detect PII in text using regex patterns"""
        results = {}
        
        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            if matches:
                results[pii_type] = [match.group() for match in matches]

        return results