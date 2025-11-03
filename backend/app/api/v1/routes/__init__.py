# app/api/v1/routes/api_router.py

from fastapi import APIRouter
from app.api.v1.routes.project_api import router as project_router
from app.api.v1.routes.ingest_api import router as ingest_router
from app.api.v1.routes.chat_api import router as chat_router

api_router = APIRouter()

api_router.include_router(project_router, prefix="/projects", tags=["projects"])
api_router.include_router(ingest_router, prefix="/ingest", tags=["ingest"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
