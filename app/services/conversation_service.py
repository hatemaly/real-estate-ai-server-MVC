# src/services/conversation_service.py
from typing import List, Optional
from app.models.conversation_models.conversation import Conversation
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(self, repository: ConversationRepository):
        self.repository = repository

    async def create_conversation(self, conversation: Conversation) -> Conversation:
        await self.repository.save(conversation)
        return conversation

    async def update_conversation(self, conversation: Conversation) -> Conversation:
        await self.repository.update(conversation)
        return conversation

    async def delete_conversation(self, conversation_id: str) -> None:
        await self.repository.delete(conversation_id)

    async def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        return await self.repository.get_by_id(conversation_id)

    async def get_conversation_history(self, conversation_id: str, limit: int = 10, offset: int = 0) -> Conversation:
        return await self.repository.retrieve_conversation_history_by_id(conversation_id, limit, offset)

    async def get_conversations_by_user_id(self, user_id: str) -> List[Conversation]:
        return await self.repository.retrieve_conversation_info_by_user_id(user_id)
