from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class DocumentChunk:
    id: str
    content: str
    source: str
    embedding: List[float]
    created_at: datetime


@dataclass
class ConversationTurn:
    role: str
    content: str
    timestamp: datetime
