from typing import List

from app.domain.entities import DocumentChunk
from app.infrastructure.vector_store import VectorStore
from app.services.llm_service import LLMService, LLMResponse


class RAGService:
    def __init__(self, vector_store: VectorStore | None = None) -> None:
        self._vector_store = vector_store or VectorStore()
        self._llm = LLMService()

    def ingest(self, chunks: List[DocumentChunk]) -> int:
        return self._vector_store.add_documents(chunks)

    async def answer(self, question: str, top_k: int = 4) -> LLMResponse:
        docs = self._vector_store.similarity_search(question, k=top_k)
        context = "\n\n".join(
            f"Source: {doc['metadata'].get('source', 'unknown')}\n{doc['content']}" for doc in docs
        )
        response = await self._llm.generate(question, context)
        response.citations = [doc["metadata"].get("source", "unknown") for doc in docs]
        return response
