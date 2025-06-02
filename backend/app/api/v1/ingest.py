import uuid
from datetime import datetime

from fastapi import APIRouter

from app.domain.entities import DocumentChunk
from app.schemas.ingest import BatchIngestRequest
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()


@router.post("/batch")
async def ingest_batch(payload: BatchIngestRequest) -> dict:
    chunks = [
        DocumentChunk(
            id=str(uuid.uuid4()),
            content=doc.content,
            source=doc.source,
            embedding=[],
            created_at=datetime.utcnow(),
        )
        for doc in payload.documents
    ]
    ingested = rag_service.ingest(chunks)
    return {"ingested": ingested}
