from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.schemas import Chunk, SearchQuery, SearchResult
from app.models import models
from app.services.service_container import service_container
from app.services.interfaces.service_interfaces import EmbeddingStrategy, VectorStore

router = APIRouter()

@router.get("/{document_id}/chunks", response_model=List[Chunk])
async def list_document_chunks(
    document_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all chunks for a document"""
    chunks = db.query(models.Chunk).filter(
        models.Chunk.document_id == document_id
    ).offset(skip).limit(limit).all()
    
    return chunks

@router.post("/search", response_model=List[SearchResult])
async def search_chunks(
    query: SearchQuery,
    db: Session = Depends(get_db)
):
    """Search chunks using semantic similarity"""
    try:
        # Get services
        embedding_strategy = service_container.get_service(EmbeddingStrategy)
        vector_store = service_container.get_service(VectorStore)

        # Generate query embedding
        query_embedding = await embedding_strategy.embed_text(query.query)

        # Search vector store
        results = await vector_store.search(
            query_embedding=query_embedding,
            top_k=query.top_k
        )

        # Format results
        search_results = []
        for result in results:
            search_results.append(SearchResult(
                text=result["text"],
                metadata=result["metadata"],
                score=1.0 - result["distance"]  # Convert distance to similarity score
            ))

        return search_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{chunk_id}", response_model=Chunk)
async def get_chunk(
    chunk_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific chunk"""
    chunk = db.query(models.Chunk).filter(models.Chunk.id == chunk_id).first()
    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found")
    return chunk