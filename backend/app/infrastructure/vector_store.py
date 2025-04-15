import json
from pathlib import Path
from typing import Iterable, List

from app.core.config import get_settings
from app.domain.entities import DocumentChunk

try:
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    from langchain.embeddings import HuggingFaceEmbeddings
except ImportError:  # pragma: no cover - optional
    FAISS = None
    OpenAIEmbeddings = None
    HuggingFaceEmbeddings = None


class VectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self._index_path = Path(settings.faiss_index_path)
        self._doc_path = Path(settings.document_store_path)
        self._doc_path.parent.mkdir(parents=True, exist_ok=True)
        self._embeddings = self._load_embeddings()
        self._faiss = self._load_faiss()

    def _load_embeddings(self):
        settings = get_settings()
        if settings.openai_api_key and OpenAIEmbeddings:
            return OpenAIEmbeddings(model=settings.embedding_model)
        if HuggingFaceEmbeddings:
            return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        raise RuntimeError("No embedding backend available")

    def _load_faiss(self):
        if FAISS is None:
            return None
        if self._index_path.exists():
            return FAISS.load_local(str(self._index_path), self._embeddings, allow_dangerous_deserialization=True)
        return None

    def add_documents(self, chunks: Iterable[DocumentChunk]) -> int:
        docs = [{"page_content": c.content, "metadata": {"source": c.source, "id": c.id}} for c in chunks]
        if FAISS is None:
            raise RuntimeError("FAISS not installed")
        if self._faiss is None:
            self._faiss = FAISS.from_texts([d["page_content"] for d in docs], self._embeddings)
        else:
            self._faiss.add_texts([d["page_content"] for d in docs])
        self._faiss.save_local(str(self._index_path))
        with self._doc_path.open("a", encoding="utf-8") as handle:
            for doc in docs:
                handle.write(json.dumps(doc) + "\n")
        return len(docs)

    def similarity_search(self, query: str, k: int = 4) -> List[dict]:
        if self._faiss is None:
            return []
        results = self._faiss.similarity_search(query, k=k)
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in results
        ]
