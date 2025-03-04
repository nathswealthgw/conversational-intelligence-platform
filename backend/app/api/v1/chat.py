from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()
conversation_service = ConversationService()


@router.post("/ask", response_model=ChatResponse)
async def ask(payload: ChatRequest) -> ChatResponse:
    conversation_service.append_turn(payload.conversation_id, "user", payload.question)
    response = await rag_service.answer(payload.question, top_k=payload.top_k)
    conversation_service.append_turn(payload.conversation_id, "assistant", response.content)
    return ChatResponse(answer=response.content, citations=response.citations)
