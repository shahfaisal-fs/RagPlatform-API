from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.schemas import PipelineCreate, Pipeline
from app.models import models

router = APIRouter()

@router.post("/", response_model=Pipeline)
async def create_pipeline(
    pipeline: PipelineCreate,
    db: Session = Depends(get_db)
):
    """Create a new pipeline"""
    db_pipeline = models.Pipeline(
        name=pipeline.name,
        description=pipeline.description,
        steps=pipeline.steps
    )
    db.add(db_pipeline)
    db.commit()
    db.refresh(db_pipeline)
    return db_pipeline

@router.get("/", response_model=List[Pipeline])
async def list_pipelines(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all pipelines"""
    pipelines = db.query(models.Pipeline).offset(skip).limit(limit).all()
    return pipelines

@router.get("/{pipeline_id}", response_model=Pipeline)
async def get_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific pipeline"""
    pipeline = db.query(models.Pipeline).filter(models.Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline

@router.put("/{pipeline_id}", response_model=Pipeline)
async def update_pipeline(
    pipeline_id: int,
    pipeline_update: PipelineCreate,
    db: Session = Depends(get_db)
):
    """Update a pipeline"""
    db_pipeline = db.query(models.Pipeline).filter(models.Pipeline.id == pipeline_id).first()
    if not db_pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    db_pipeline.name = pipeline_update.name
    db_pipeline.description = pipeline_update.description
    db_pipeline.steps = pipeline_update.steps

    db.commit()
    db.refresh(db_pipeline)
    return db_pipeline

@router.delete("/{pipeline_id}")
async def delete_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db)
):
    """Delete a pipeline"""
    pipeline = db.query(models.Pipeline).filter(models.Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    db.delete(pipeline)
    db.commit()
    return {"message": "Pipeline deleted successfully"}