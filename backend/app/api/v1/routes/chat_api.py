from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.chat import ChatRequest
from app.models.project import Project
from app.services.pipeline.service_container import ServiceContainer
from app.services.pipeline.pipeline_runtime import PipelineRuntime
import os
import logging

logger = logging.getLogger(__name__)

TENANT = os.environ.get("TENANT_ID","airline")
router = APIRouter(prefix="/api/v1", tags=["chat"])
'''
@router.post("/chat")
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    p = db.query(Project).filter_by(project_id=req.project_id).first()
    if not p: raise HTTPException(404, "project not found")
    container = ServiceContainer(p.pipeline)
    meta = {"tenant": TENANT, "department": req.department, "project_id": p.project_id}
    result = await PipelineRuntime.answer(container, req.query, meta, req.top_k)
    return result
'''

@router.post("/chat")
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        pipeline_cfg = {
        "chunker": "recursive",
        "embedder": "azure-openai",
        "vector_store": "azure-search",
        "reranker": "none",
        "pii": "regex",
        "governance": "basic",
        "llm": "azure-openai",
        "chunk_size": 800,
        "chunk_overlap": 100
    }
    
        container = ServiceContainer(pipeline_cfg)

        meta = {
            "tenant": TENANT,
            "department": req.department,
            "project_id": req.project_id,
            "group_ids": ["Team-AI"],
            "owner_user_id": "unknown"
        }

    

        logger.info("Chat request received: %s", req.model_dump())
        result = await PipelineRuntime.answer(container, req.query, meta, req.top_k)
        logger.info("Chat response generated")
        return result


    except Exception as e:
        logger.exception("Chat error occurred!")  # Full traceback logged
        raise HTTPException(status_code=500, detail=str(e))

