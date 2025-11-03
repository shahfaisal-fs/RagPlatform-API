from typing import Dict, Any
from app.services.interfaces.data_governance import DataGovernance

class BasicGovernance(DataGovernance):
    async def validate_document(self, content: str, metadata: Dict[str, Any]) -> bool:
        # Example: reject if PII found
        return not bool(metadata.get("pii"))
