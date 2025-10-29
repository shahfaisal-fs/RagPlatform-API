from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    name: str
    doc_metadata: Dict[str, Any] = Field(default_factory=dict)

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChunkBase(BaseModel):
    content: str
    chunk_metadata: Dict[str, Any] = Field(default_factory=dict)

class ChunkCreate(ChunkBase):
    document_id: int

class Chunk(ChunkBase):
    id: int
    document_id: int
    embedding: Optional[List[float]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PipelineBase(BaseModel):
    name: str
    description: str
    steps: List[Dict[str, Any]]

class PipelineCreate(PipelineBase):
    pass

class Pipeline(PipelineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    query: str
    top_k: int = 5
    filter_metadata: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    text: str
    metadata: Dict[str, Any]
    score: float

class ProcessingResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None