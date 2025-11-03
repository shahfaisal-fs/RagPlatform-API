from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.project import ProjectCreate
from app.models.project import Project

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])

@router.post("")
def create_project(req: ProjectCreate, db: Session = Depends(get_db)):
    exists = db.query(Project).filter_by(project_id=req.project_id).first()
    if exists:
        raise HTTPException(400, "project_id already exists")
    p = Project(project_id=req.project_id, tenant=req.tenant, department=req.department, pipeline=req.pipeline)
    db.add(p); db.commit(); db.refresh(p)
    return {"status":"created","project_id":p.project_id}
