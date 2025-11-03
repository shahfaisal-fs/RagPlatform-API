from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class IngestRequest(BaseModel):
    project_id: str
    text: str
    source: str = "Upload"
    # NEW metadata:
    tenant: str
    department: str
    classification: str = "Internal"           # Internal | Confidential | Public
    visibility: str = "Shared"                 # Public | Shared | Private
    owner_user_id: str
    group_ids: List[str] = Field(default_factory=list)
    doc_metadata: Dict[str, Any] = Field(default_factory=dict)
