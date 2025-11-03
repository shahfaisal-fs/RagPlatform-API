from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base

class PIIEntity(Base):
    __tablename__ = "pii_entities"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    doc_key = Column(String(256), index=True)  # same key we use for chunks base
    token_id = Column(String(64), index=True)  # E:person:abc123
    entity_type = Column(String(64))           # person | email | phone | id
    raw_encrypted = Column(Text)               # AES-GCM ciphertext (base64/hex)
    created_at = Column(DateTime, default=datetime.utcnow)