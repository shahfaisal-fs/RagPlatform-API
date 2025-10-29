from fastapi import APIRouter
from app.api.v1.routes import documents, pipelines, embeddings, chunks

api_router = APIRouter()

api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["pipelines"])
api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
api_router.include_router(chunks.router, prefix="/chunks", tags=["chunks"])