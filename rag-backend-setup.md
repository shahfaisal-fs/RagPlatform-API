# RAG Studio — FastAPI Control Plane (Complete Scaffold)

## ✅ Goal
Generate a **runnable FastAPI backend** with full **Strategy/Factory architecture**:
- Interfaces + implementations for: Chunking, Embedding, VectorStore, LLM, PII Filter, Governance
- Multiple Governance strategies (Strict/Lenient/AuditOnly) — easily extendable
- Multi-cloud provider adapters (Azure/AWS/OnPrem) — dummy, swappable via config
- Minimal deps; SQLite; no external AI calls (mocked)
- Endpoints aligned to RAG Studio UI

Ensure the app runs with:
uvicorn app.main:app --reload


---

## 📦 Dependencies (create `requirements.txt`)
Use minimal packages to work in restricted environments.


fastapi
uvicorn
pydantic
sqlalchemy
python-jose
passlib[bcrypt]


Create a `.env` (even if blank for now):


JWT_SECRET=dev-secret
JWT_ALG=HS256


---

## 📁 Project Structure (generate exactly)



backend/
├─ app/
│ ├─ main.py
│ ├─ core/
│ │ ├─ config.py
│ │ ├─ security.py
│ │ └─ logger.py
│ ├─ api/
│ │ └─ v1/
│ │ ├─ routes/
│ │ │ ├─ auth.py
│ │ │ ├─ projects.py
│ │ │ ├─ connectors.py
│ │ │ ├─ ingest.py
│ │ │ ├─ retrieval.py
│ │ │ └─ chat.py
│ │ └─ init.py
│ ├─ services/
│ │ ├─ factories.py
│ │ ├─ governance/
│ │ │ ├─ base.py
│ │ │ ├─ strict.py
│ │ │ ├─ lenient.py
│ │ │ ├─ audit_only.py
│ │ │ └─ init.py
│ │ ├─ pii/
│ │ │ ├─ base.py
│ │ │ ├─ regex_filter.py
│ │ │ ├─ none_filter.py
│ │ │ └─ init.py
│ │ ├─ chunking/
│ │ │ ├─ base.py
│ │ │ ├─ recursive.py
│ │ │ ├─ paragraph.py
│ │ │ ├─ semantic.py
│ │ │ └─ init.py
│ │ ├─ embedding/
│ │ │ ├─ base.py
│ │ │ ├─ azure_openai.py
│ │ │ ├─ aws_bedrock.py
│ │ │ ├─ onprem_hf.py
│ │ │ └─ dummy_provider.py
│ │ ├─ vectorstore/
│ │ │ ├─ base.py
│ │ │ ├─ azure_cognitive.py
│ │ │ ├─ opensearch.py
│ │ │ ├─ pgvector.py
│ │ │ └─ dummy_store.py
│ │ ├─ llm/
│ │ │ ├─ base.py
│ │ │ ├─ azure_gpt.py
│ │ │ ├─ claude_bedrock.py
│ │ │ ├─ onprem_hf.py
│ │ │ └─ dummy_llm.py
│ │ ├─ connectors/
│ │ │ ├─ base.py
│ │ │ ├─ confluence.py
│ │ │ ├─ sharepoint.py
│ │ │ └─ init.py
│ ├─ models/
│ │ ├─ user.py
│ │ ├─ project.py
│ │ ├─ rag_config.py
│ │ └─ init.py
│ ├─ schemas/
│ │ ├─ auth.py
│ │ ├─ project.py
│ │ ├─ rag_config.py
│ │ ├─ chat.py
│ │ └─ init.py
│ ├─ database/
│ │ ├─ session.py
│ │ ├─ base.py
│ │ └─ init.py
│ ├─ deps/
│ │ ├─ auth_deps.py
│ │ └─ governance_deps.py
│ └─ init.py
├─ .env
├─ requirements.txt
└─ README.md


---

## 🧩 Core Files — put these exact contents

### `app/core/config.py`
```python
from pydantic import BaseModel
import os

class Settings(BaseModel):
    PROJECT_NAME: str = "RAG Studio API"
    API_PREFIX: str = "/api/v1"
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret")
    JWT_ALG: str = os.getenv("JWT_ALG", "HS256")

settings = Settings()

app/core/security.py
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(sub: str, minutes: int = 60):
    payload = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=minutes)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

app/core/logger.py
import logging
logger = logging.getLogger("rag")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./backend.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

app/database/base.py
from sqlalchemy.orm import declarative_base
Base = declarative_base()

👥 Models
app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String, default="user")  # admin | manager | user

app/models/project.py
from sqlalchemy import Column, Integer, String, JSON
from app.database.base import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    rag_config = Column(JSON)  # stores config dict

app/models/rag_config.py
# Placeholder model kept as schema-driven; config stored on Project.rag_config

🧾 Schemas
app/schemas/auth.py
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

app/schemas/project.py
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ProjectCreate(BaseModel):
    name: str
    department: str
    rag_config: Dict[str, Any]

class ProjectOut(BaseModel):
    id: int
    name: str
    department: str
    rag_config: Dict[str, Any]

    class Config:
        from_attributes = True

app/schemas/rag_config.py
from pydantic import BaseModel
from typing import Optional

class RAGConfig(BaseModel):
    cloud: str                     # azure | aws | onprem
    vector_store: str              # azure_cognitive | opensearch | pgvector | dummy
    embedding_provider: str        # azure_openai | aws_bedrock | onprem_hf | dummy
    chunking_strategy: str         # recursive | paragraph | semantic
    llm_provider: str              # azure_gpt | claude_bedrock | onprem_hf | dummy
    pii_filter: str                # regex | none
    governance_policy: str         # strict | lenient | audit_only
    retriever_top_k: int = 5

app/schemas/chat.py
from pydantic import BaseModel
from typing import List, Dict, Any

class SearchRequest(BaseModel):
    project_id: int
    query: str
    top_k: int = 5

class ChunkOut(BaseModel):
    text: str
    metadata: Dict[str, Any]

class ChatRequest(BaseModel):
    project_id: int
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[ChunkOut]

🔐 Deps
app/deps/auth_deps.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# For demo, accept any token "demo"
security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    # In real system: validate JWT + fetch claims
    if not token or not token.credentials:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Fake user
    return {"email": "faisal@example.com", "role": "admin", "departments": ["HR","Finance","Ops"]}

app/deps/governance_deps.py
from app.services.governance.base import IGovernancePolicy
from app.services.governance.strict import StrictGovernance
from app.services.governance.lenient import LenientGovernance
from app.services.governance.audit_only import AuditOnlyGovernance

def governance_from_name(name: str) -> IGovernancePolicy:
    mapping = {
        "strict": StrictGovernance(),
        "lenient": LenientGovernance(),
        "audit_only": AuditOnlyGovernance()
    }
    return mapping.get(name, StrictGovernance())

🧠 Services — Interfaces & Implementations
Governance

app/services/governance/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class IGovernancePolicy(ABC):
    @abstractmethod
    def authorize(self, user: Dict[str, Any], resource: Dict[str, Any], action: str) -> bool: ...
    @abstractmethod
    def name(self) -> str: ...


app/services/governance/strict.py

from .base import IGovernancePolicy

class StrictGovernance(IGovernancePolicy):
    def authorize(self, user, resource, action: str) -> bool:
        # Allow admin; otherwise enforce exact department match
        if user.get("role") == "admin":
            return True
        return resource.get("department") in user.get("departments", [])
    def name(self) -> str:
        return "strict"


app/services/governance/lenient.py

from .base import IGovernancePolicy

class LenientGovernance(IGovernancePolicy):
    def authorize(self, user, resource, action: str) -> bool:
        # Allow if department overlaps OR action is 'read'
        if user.get("role") == "admin":
            return True
        if action == "read":
            return True
        return resource.get("department") in user.get("departments", [])
    def name(self) -> str:
        return "lenient"


app/services/governance/audit_only.py

from .base import IGovernancePolicy

class AuditOnlyGovernance(IGovernancePolicy):
    def authorize(self, user, resource, action: str) -> bool:
        # Always allow but assume system logs everything (logging done at route)
        return True
    def name(self) -> str:
        return "audit_only"

PII Filter

app/services/pii/base.py

from abc import ABC, abstractmethod
from typing import List

class IPIIFilter(ABC):
    @abstractmethod
    def apply(self, chunks: List[str]) -> List[str]: ...


app/services/pii/regex_filter.py

import re
from typing import List
from .base import IPIIFilter

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\+?\d[\d\- ]{7,}\d")

class RegexPIIFilter(IPIIFilter):
    def apply(self, chunks: List[str]) -> List[str]:
        out = []
        for c in chunks:
            c = EMAIL.sub("[REDACTED_EMAIL]", c)
            c = PHONE.sub("[REDACTED_PHONE]", c)
            out.append(c)
        return out


app/services/pii/none_filter.py

from typing import List
from .base import IPIIFilter

class NoPIIFilter(IPIIFilter):
    def apply(self, chunks: List[str]) -> List[str]:
        return chunks

Chunking

app/services/chunking/base.py

from abc import ABC, abstractmethod
from typing import List

class IChunkingStrategy(ABC):
    @abstractmethod
    def chunk(self, text: str) -> List[str]: ...


app/services/chunking/recursive.py

from .base import IChunkingStrategy

class RecursiveChunking(IChunkingStrategy):
    def __init__(self, max_tokens=500, overlap=50):
        self.max_tokens = max_tokens
        self.overlap = overlap
    def chunk(self, text: str):
        step = max(self.max_tokens - self.overlap, 1)
        return [ text[i:i+self.max_tokens] for i in range(0, len(text), step) ]


app/services/chunking/paragraph.py

from .base import IChunkingStrategy

class ParagraphChunking(IChunkingStrategy):
    def chunk(self, text: str):
        return [p.strip() for p in text.split("\n\n") if p.strip()]


app/services/chunking/semantic.py

from .base import IChunkingStrategy

class SemanticChunking(IChunkingStrategy):
    def chunk(self, text: str):
        # Placeholder: naive split by sentences
        return [s.strip() for s in text.split(". ") if s.strip()]

Embedding

app/services/embedding/base.py

from abc import ABC, abstractmethod
from typing import List

class IEmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, chunks: List[str]) -> List[list[float]]: ...


app/services/embedding/dummy_provider.py

import math
from typing import List
from .base import IEmbeddingProvider

class DummyEmbedding(IEmbeddingProvider):
    async def embed(self, chunks: List[str]) -> List[list[float]]:
        # Deterministic tiny vectors
        vecs = []
        for c in chunks:
            s = sum(ord(ch) for ch in c) or 1
            vecs.append([ (s % 101)/100.0, (s % 97)/100.0, math.sin(s)%1 ])
        return vecs


(Keep azure_openai.py, aws_bedrock.py, onprem_hf.py as stubs returning NotImplementedError with TODOs.)

VectorStore

app/services/vectorstore/base.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IVectorStore(ABC):
    @abstractmethod
    def upsert(self, vectors: List[Dict[str, Any]]): ...
    @abstractmethod
    def search(self, query_vector: list[float], top_k: int) -> List[Dict[str, Any]]: ...


app/services/vectorstore/dummy_store.py

from typing import List, Dict, Any
from .base import IVectorStore

# In-memory store per project
MEM: Dict[str, List[Dict[str, Any]]] = {}

class DummyVectorStore(IVectorStore):
    def __init__(self, namespace: str):
        self.ns = namespace
        MEM.setdefault(self.ns, [])

    def upsert(self, vectors: List[Dict[str, Any]]):
        MEM[self.ns].extend(vectors)

    def search(self, query_vector: list[float], top_k: int) -> List[Dict[str, Any]]:
        # naive: return last K
        return list(reversed(MEM.get(self.ns, [])))[:top_k]


(Leave azure_cognitive.py, opensearch.py, pgvector.py as TODO stubs.)

LLM

app/services/llm/base.py

from abc import ABC, abstractmethod

class ILLMProvider(ABC):
    @abstractmethod
    async def generate(self, query: str, context: str) -> str: ...


app/services/llm/dummy_llm.py

from .base import ILLMProvider

class DummyLLM(ILLMProvider):
    async def generate(self, query: str, context: str) -> str:
        return f"[MOCK ANSWER]\nQ: {query}\nBased on context:\n{context[:300]}..."

Connectors (stubs)

app/services/connectors/base.py

from abc import ABC, abstractmethod
from typing import List

class IDataConnector(ABC):
    @abstractmethod
    def list_documents(self) -> List[str]: ...
    @abstractmethod
    def fetch_content(self, doc_id: str) -> str: ...


app/services/connectors/confluence.py

from .base import IDataConnector

class ConfluenceConnector(IDataConnector):
    def list_documents(self): return ["conf:doc1","conf:doc2"]
    def fetch_content(self, doc_id: str): return f"Confluence content for {doc_id}"


app/services/connectors/sharepoint.py

from .base import IDataConnector

class SharePointConnector(IDataConnector):
    def list_documents(self): return ["sp:docA","sp:docB"]
    def fetch_content(self, doc_id: str): return f"SharePoint content for {doc_id}"

🏗️ Factories

app/services/factories.py

from typing import Dict, Any
# Chunking
from app.services.chunking.recursive import RecursiveChunking
from app.services.chunking.paragraph import ParagraphChunking
from app.services.chunking.semantic import SemanticChunking
# Embedding
from app.services.embedding.dummy_provider import DummyEmbedding
# Vector
from app.services.vectorstore.dummy_store import DummyVectorStore
# LLM
from app.services.llm.dummy_llm import DummyLLM
# PII
from app.services.pii.regex_filter import RegexPIIFilter
from app.services.pii.none_filter import NoPIIFilter
# Governance
from app.services.governance.strict import StrictGovernance
from app.services.governance.lenient import LenientGovernance
from app.services.governance.audit_only import AuditOnlyGovernance

def get_chunker(cfg: Dict[str, Any]):
    m = (cfg.get("chunking_strategy") or "recursive").lower()
    return {"recursive": RecursiveChunking(),
            "paragraph": ParagraphChunking(),
            "semantic": SemanticChunking()}.get(m, RecursiveChunking())

def get_embedder(cfg: Dict[str, Any]):
    # Swap to real providers later per cfg
    return DummyEmbedding()

def get_vector_store(cfg: Dict[str, Any], namespace: str):
    # Swap to Azure/OpenSearch/PG later per cfg
    return DummyVectorStore(namespace)

def get_llm(cfg: Dict[str, Any]):
    return DummyLLM()

def get_pii_filter(cfg: Dict[str, Any]):
    name = (cfg.get("pii_filter") or "none").lower()
    return {"regex": RegexPIIFilter(),
            "none": NoPIIFilter()}.get(name, NoPIIFilter())

def get_governance(cfg: Dict[str, Any]):
    pol = (cfg.get("governance_policy") or "strict").lower()
    return {"strict": StrictGovernance(),
            "lenient": LenientGovernance(),
            "audit_only": AuditOnlyGovernance()}.get(pol, StrictGovernance())

🧭 API Routes
app/api/v1/routes/auth.py
from fastapi import APIRouter
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    token = create_access_token(body.email)
    return TokenResponse(access_token=token)

app/api/v1/routes/projects.py
from fastapi import APIRouter, Depends
from typing import List
from app.schemas.project import ProjectCreate, ProjectOut
from app.database.session import SessionLocal
from app.database.base import Base
from app.models.project import Project
from app.models.user import User
from sqlalchemy import select
from app.deps.auth_deps import get_current_user

router = APIRouter()

# init DB tables on first import
from sqlalchemy import create_engine
engine = create_engine("sqlite:///./backend.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

@router.get("", response_model=List[ProjectOut])
def list_projects(user=Depends(get_current_user)):
    with SessionLocal() as db:
        rows = db.execute(select(Project)).scalars().all()
        return rows

@router.post("", response_model=ProjectOut)
def create_project(body: ProjectCreate, user=Depends(get_current_user)):
    with SessionLocal() as db:
        p = Project(name=body.name, department=body.department, rag_config=body.rag_config)
        db.add(p); db.commit(); db.refresh(p)
        return p

app/api/v1/routes/ingest.py
from fastapi import APIRouter, Depends, HTTPException
from app.database.session import SessionLocal
from app.models.project import Project
from sqlalchemy import select
from app.services.factories import get_chunker, get_embedder, get_vector_store, get_pii_filter
from app.deps.auth_deps import get_current_user
from app.deps.governance_deps import governance_from_name

router = APIRouter()

@router.post("/{project_id}")
def ingest_project(project_id: int, user=Depends(get_current_user)):
    # Load project & config
    with SessionLocal() as db:
        prj = db.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()
        if not prj:
            raise HTTPException(404, "Project not found")

        cfg = prj.rag_config or {}
        gov = governance_from_name(cfg.get("governance_policy","strict"))
        resource = {"department": prj.department, "project_id": prj.id}
        if not gov.authorize(user, resource, "ingest"):
            raise HTTPException(403, "Forbidden by governance policy")

        # Mock single doc
        text = f"Sample document for project {prj.name} in {prj.department}."
        chunker = get_chunker(cfg); chunks = chunker.chunk(text)
        pii = get_pii_filter(cfg); chunks = pii.apply(chunks)
        embedder = get_embedder(cfg)
        vectors = [{"id": f"{prj.id}-{i}", "text": c, "vector": v, "metadata": {"project": prj.name, "dept": prj.department}}
                   for i,(c,v) in enumerate(zip(chunks, awaitable(embedder.embed(chunks))))]
        store = get_vector_store(cfg, namespace=f"proj:{prj.id}")
        store.upsert(vectors)
        return {"status": "ingest_ok", "chunks": len(chunks)}

# Helper to await async in sync route (simple)
import asyncio
def awaitable(coro): return asyncio.get_event_loop().run_until_complete(coro)

app/api/v1/routes/retrieval.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.database.session import SessionLocal
from app.models.project import Project
from app.schemas.chat import SearchRequest, ChunkOut
from app.services.factories import get_embedder, get_vector_store
from app.deps.auth_deps import get_current_user
from app.deps.governance_deps import governance_from_name

router = APIRouter()

@router.post("/search")
def search(body: SearchRequest, user=Depends(get_current_user)):
    with SessionLocal() as db:
        prj = db.execute(select(Project).where(Project.id==body.project_id)).scalar_one_or_none()
        if not prj: raise HTTPException(404, "Project not found")
        cfg = prj.rag_config or {}
        gov = governance_from_name(cfg.get("governance_policy","strict"))
        resource = {"department": prj.department, "project_id": prj.id}
        if not gov.authorize(user, resource, "read"):
            raise HTTPException(403, "Forbidden by governance policy")

        embedder = get_embedder(cfg)
        qv = awaitable(embedder.embed([body.query]))[0]
        store = get_vector_store(cfg, namespace=f"proj:{prj.id}")
        hits = store.search(qv, body.top_k)
        return [ChunkOut(text=h["text"], metadata=h["metadata"]) for h in hits]

app/api/v1/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.database.session import SessionLocal
from app.models.project import Project
from app.schemas.chat import ChatRequest, ChatResponse, ChunkOut
from app.services.factories import get_embedder, get_vector_store, get_llm
from app.deps.auth_deps import get_current_user
from app.deps.governance_deps import governance_from_name

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
def chat(body: ChatRequest, user=Depends(get_current_user)):
    with SessionLocal() as db:
        prj = db.execute(select(Project).where(Project.id==body.project_id)).scalar_one_or_none()
        if not prj: raise HTTPException(404, "Project not found")
        cfg = prj.rag_config or {}
        gov = governance_from_name(cfg.get("governance_policy","strict"))
        resource = {"department": prj.department, "project_id": prj.id}
        if not gov.authorize(user, resource, "read"):
            raise HTTPException(403, "Forbidden by governance policy")

        embedder = get_embedder(cfg)
        qv = awaitable(embedder.embed([body.query]))[0]
        store = get_vector_store(cfg, namespace=f"proj:{prj.id}")
        hits = store.search(qv, cfg.get("retriever_top_k", 5))
        context = "\n\n".join(h["text"] for h in hits)
        llm = get_llm(cfg)
        answer = awaitable(llm.generate(body.query, context))
        return ChatResponse(
            answer=answer,
            sources=[ChunkOut(text=h["text"], metadata=h["metadata"]) for h in hits]
        )

import asyncio
def awaitable(coro): return asyncio.get_event_loop().run_until_complete(coro)

app/api/v1/routes/connectors.py (stub)
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def list_connectors():
    return [{"id":"conf","type":"confluence"},{"id":"sp","type":"sharepoint"}]

🚀 Main App
app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.routes import auth, projects, connectors, ingest, retrieval, chat

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["Auth"])
app.include_router(projects.router, prefix=f"{settings.API_PREFIX}/projects", tags=["Projects"])
app.include_router(connectors.router, prefix=f"{settings.API_PREFIX}/connectors", tags=["Connectors"])
app.include_router(ingest.router, prefix=f"{settings.API_PREFIX}/ingest", tags=["Ingest"])
app.include_router(retrieval.router, prefix=f"{settings.API_PREFIX}/retrieval", tags=["Retrieval"])
app.include_router(chat.router, prefix=f"{settings.API_PREFIX}/chat", tags=["Chat"])

@app.get("/")
def root():
    return {"status": "RAG backend running"}

README.md (short)

Create venv

pip install -r requirements.txt

Run: uvicorn app.main:app --reload

Open: http://localhost:8000/docs

Flow:

POST /api/v1/auth/login → get token (use in Authorize button on docs)

POST /api/v1/projects with a sample rag_config

POST /api/v1/ingest/{projectId}

POST /api/v1/retrieval/search

POST /api/v1/chat/query

Sample rag_config for project creation:

{
  "cloud": "azure",
  "vector_store": "dummy",
  "embedding_provider": "dummy",
  "chunking_strategy": "paragraph",
  "llm_provider": "dummy",
  "pii_filter": "regex",
  "governance_policy": "strict",
  "retriever_top_k": 5
}

Final Action

Create all files exactly as above and ensure:

uvicorn app.main:app --reload


works, and the OpenAPI docs show the routes under /api/v1/*.

@workspace
Generate all files/code above now.