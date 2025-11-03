from datetime import datetime
from sqlalchemy import Column, BigInteger, Integer, String, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class IngestionLog(Base):
    __tablename__ = "ingestion_logs"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(String(128), index=True)
    project_id = Column(String(128), index=True)
    department = Column(String(128), index=True)
    source_system = Column(String(128))
    visibility = Column(String(32))
    classification = Column(String(64))
    owner_user_id = Column(String(256), index=True)
    groups = Column(JSON)             # ["Team-AI", ...]
    doc_key = Column(String(256))     # index doc id prefix/base
    chunk_count = Column(Integer)
    pii_found = Column(Boolean, default=False)
    pii_summary = Column(JSON, default={})  # {"person":2, "email":1, ...}
    policy_decision = Column(String(64))    # "allowed" | "blocked" | "masked"
    created_at = Column(DateTime, default=datetime.utcnow)