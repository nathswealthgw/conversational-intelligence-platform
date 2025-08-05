from datetime import datetime
from typing import List

from app.domain.entities import ConversationTurn


class ConversationService:
    def __init__(self) -> None:
        self._store: dict[str, List[ConversationTurn]] = {}

    def append_turn(self, conversation_id: str, role: str, content: str) -> None:
        turns = self._store.setdefault(conversation_id, [])
        turns.append(ConversationTurn(role=role, content=content, timestamp=datetime.utcnow()))

    def history(self, conversation_id: str) -> List[ConversationTurn]:
        return self._store.get(conversation_id, [])
