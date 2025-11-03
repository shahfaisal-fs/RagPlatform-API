from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.ingest import IngestRequest
from app.models.project import Project
from app.services.pipeline.service_container import ServiceContainer
from app.services.pipeline.pipeline_runtime import PipelineRuntime
import os

TENANT = os.environ.get("TENANT_ID","airline")
router = APIRouter(prefix="/api/v1", tags=["ingest"])
"""
@router.post("/ingest")
async def ingest(req: IngestRequest, db: Session = Depends(get_db)):
    p = db.query(Project).filter_by(project_id=req.project_id).first()
    if not p: raise HTTPException(404, "project not found")
    container = ServiceContainer(p.pipeline)
    meta = {"tenant": TENANT, "department": p.department, "project_id": p.project_id, "source": req.source}
    count = await PipelineRuntime.ingest(container, req.text, meta)
    if count == 0: raise HTTPException(400, "Ingestion failed (governance/PII/chunking)")
    return {"status":"ingestion_complete","chunks_indexed":count}*/
"""

@router.post("/ingest")
async def ingest(req: IngestRequest, db: Session = Depends(get_db)):
    """
    TEMPORARY: Hardcoded pipeline config for Azure connectivity testing.
    Replace after Project DB setup works.
    """

    try:

        # Hardcoded pipeline configuration
        pipeline_cfg = {
            "chunker": "recursive",
            "embedder": "azure-openai",
            "vector_store": "azure-search",
            "reranker": "none",
            "pii": "regex",
            "pseudonymizer": "simple", 
            "governance": "basic",
            "llm": "azure-openai",
            "chunk_size": 800,
            "chunk_overlap": 100
    }

        # Create pipeline service container dynamically
        container = ServiceContainer(pipeline_cfg)

        # Temporary project mock object (until DB fully wired)
        p = type("obj", (object,), {
            "department": "Engineering",
            "project_id": req.project_id
        })

        # Metadata used for governance + storage filtering
        meta = {
            "tenant": TENANT,
            "department": p.department,
            "project_id": p.project_id,
            "source": req.source
        }

        # Run runtime ingestion
        count = await PipelineRuntime.ingest(container, req.text, meta)
        #count = await PipelineRuntime.ingest(container, req.text, meta,db)


        if count == 0:
            raise HTTPException(400, "Ingestion blocked by policy or produced 0 chunks.")
        return {"status": "ingestion_complete", "chunks_indexed": count}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))