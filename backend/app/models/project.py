from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from app.database.database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    project_id = Column(String, unique=True, index=True)
    tenant = Column(String, index=True)
    department = Column(String, index=True)
    # pipeline config (which strategies)
    pipeline = Column(JSON)  # { chunker, embedder, vector_store, reranker, pii_detector, governance, llm, chunk_size, chunk_overlap, retriever_top_k }
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
