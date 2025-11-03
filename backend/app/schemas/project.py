from pydantic import BaseModel
from typing import Dict, Any

class ProjectCreate(BaseModel):
    project_id: str
    tenant: str
    department: str
    pipeline: Dict[str, Any]
