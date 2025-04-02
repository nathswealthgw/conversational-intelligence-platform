from dataclasses import dataclass
from typing import List

from app.core.config import get_settings

try:
    from langchain_openai import ChatOpenAI
except ImportError:  # pragma: no cover
    ChatOpenAI = None


@dataclass
class LLMResponse:
    content: str
    citations: List[str]


class LLMService:
    def __init__(self) -> None:
        settings = get_settings()
        self._settings = settings
        if settings.openai_api_key and ChatOpenAI:
            self._client = ChatOpenAI(model=settings.llm_model, temperature=0.1)
        else:
            self._client = None

    async def generate(self, question: str, context: str) -> LLMResponse:
        prompt = (
            "You are a virtual analyst. Use the provided context to answer precisely. "
            "If the answer is not in the context, say you don't know.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        if self._client:
            response = await self._client.apredict(prompt)
            return LLMResponse(content=response, citations=[])
        return LLMResponse(
            content=(
                "[Mock Response] Configure OPENAI_API_KEY to enable real answers. "
                "Based on context: " + context[:200]
            ),
            citations=[],
        )
