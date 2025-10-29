from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from typing import List
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.schemas import DocumentCreate, Document, ProcessingResponse
from app.models import models
from app.services.service_container import service_container
from app.services.interfaces.service_interfaces import (
    DocumentProcessor, ChunkStrategy, EmbeddingStrategy,
    VectorStore, PIIDetector, DataGovernance
)

router = APIRouter()

@router.post("/upload", response_model=ProcessingResponse)
async def upload_document(
    file: UploadFile = File(...),
    metadata: DocumentCreate = None,
    db: Session = Depends(get_db)
):
    """
    Upload and process a document:
    1. Process document
    2. Check for PII
    3. Apply governance rules
    4. Split into chunks
    5. Generate embeddings
    6. Store in vector database
    """
    try:
        # Get services
        doc_processor = service_container.get_service(DocumentProcessor)
        pii_detector = service_container.get_service(PIIDetector)
        governance = service_container.get_service(DataGovernance)
        chunk_strategy = service_container.get_service(ChunkStrategy)
        embedding_strategy = service_container.get_service(EmbeddingStrategy)
        vector_store = service_container.get_service(VectorStore)

        # Read and process document
        content = await file.read()
        doc_content = await doc_processor.process_document(content, metadata.dict() if metadata else {})

        # Check for PII
        pii_results = await pii_detector.detect_pii(doc_content)
        if pii_results:
            metadata.doc_metadata['pii_detected'] = pii_results

        # Validate against governance rules
        if not await governance.validate_document(doc_content, metadata.dict().get('doc_metadata', {})):
            raise HTTPException(status_code=400, detail="Document failed governance validation")

        # Create document in database
        db_document = models.Document(
            name=file.filename,
            content=doc_content,
            doc_metadata=metadata.dict().get('doc_metadata', {})
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        # Split into chunks
        chunks = await chunk_strategy.chunk_text(doc_content)

        # Generate embeddings and store chunks
        chunk_embeddings = []
        for chunk_text in chunks:
            # Generate embedding
            embedding = await embedding_strategy.embed_text(chunk_text)
            chunk_embeddings.append(embedding)

            # Create chunk in database
            db_chunk = models.Chunk(
                document_id=db_document.id,
                content=chunk_text,
                embedding=embedding,
                metadata={"source_doc": file.filename}
            )
            db.add(db_chunk)

        # Store in vector database
        await vector_store.add_embeddings(
            texts=chunks,
            embeddings=chunk_embeddings,
            metadata=[{"source_doc": file.filename} for _ in chunks]
        )

        db.commit()

        return ProcessingResponse(
            status="success",
            message="Document processed successfully",
            data={"document_id": db_document.id}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Document])
async def list_documents(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all documents"""
    documents = db.query(models.Document).offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific document"""
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Delete a document and its chunks"""
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete associated chunks
    db.query(models.Chunk).filter(models.Chunk.document_id == document_id).delete()
    
    # Delete document
    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}