from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base

class PolicyDecision(Base):
    __tablename__ = "policy_decisions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(String(128))
    project_id = Column(String(128))
    rule = Column(String(128))         # e.g., "block_public_with_pii"
    decision = Column(String(32))      # allow | block | mask
    reason = Column(Text)
    context = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)