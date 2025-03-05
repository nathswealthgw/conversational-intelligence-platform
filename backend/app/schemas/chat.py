from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    conversation_id: str = Field(..., example="conv-123")
    question: str = Field(..., example="What are the retention risks?")
    top_k: int = Field(4, ge=1, le=10)


class ChatResponse(BaseModel):
    answer: str
    citations: List[str]
