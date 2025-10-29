from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.schemas import Chunk
from app.models import models
from app.services.service_container import service_container
from app.services.interfaces.service_interfaces import EmbeddingStrategy

router = APIRouter()

@router.post("/{chunk_id}/generate", response_model=Chunk)
async def generate_embedding(
    chunk_id: int,
    db: Session = Depends(get_db)
):
    """Generate embedding for a specific chunk"""
    try:
        # Get chunk
        chunk = db.query(models.Chunk).filter(models.Chunk.id == chunk_id).first()
        if not chunk:
            raise HTTPException(status_code=404, detail="Chunk not found")

        # Get embedding service
        embedding_strategy = service_container.get_service(EmbeddingStrategy)

        # Generate embedding
        embedding = await embedding_strategy.embed_text(chunk.content)

        # Update chunk with new embedding
        chunk.embedding = embedding
        db.commit()
        db.refresh(chunk)

        return chunk

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/regenerate-all")
async def regenerate_all_embeddings(
    db: Session = Depends(get_db)
):
    """Regenerate embeddings for all chunks"""
    try:
        # Get embedding service
        embedding_strategy = service_container.get_service(EmbeddingStrategy)

        # Get all chunks
        chunks = db.query(models.Chunk).all()
        count = 0

        for chunk in chunks:
            # Generate new embedding
            embedding = await embedding_strategy.embed_text(chunk.content)
            
            # Update chunk
            chunk.embedding = embedding
            count += 1

        db.commit()

        return {
            "message": "Embeddings regenerated successfully",
            "chunks_processed": count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))