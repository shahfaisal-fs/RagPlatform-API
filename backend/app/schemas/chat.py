from pydantic import BaseModel

class ChatRequest(BaseModel):
    project_id: str
    department: str
    query: str
    top_k: int = 6
