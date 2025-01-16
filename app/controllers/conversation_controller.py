from typing import Optional, List

from app.models.conversation_models.conversation import Conversation
from app.schemas.conversation import ConversationCreate, ConversationUpdate
from app.services.conversation_service import ConversationService


class ConversationController:
    def __init__(self, service: ConversationService):
        self.service = service

    async def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        conversation = Conversation(**conversation_data.dict())
        return await self.service.create_conversation(conversation)

    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return await self.service.get_conversation_by_id(conversation_id)

    async def get_conversations_by_user(self, user_id: str) -> List[Conversation]:
        return await self.service.get_conversations_by_user_id(user_id)

    async def update_conversation(self, conversation_id: str, conversation_update: ConversationUpdate) -> Optional[Conversation]:
        conversation = await self.service.get_conversation_by_id(conversation_id)
        if conversation:
            if conversation_update.title:
                conversation.title = conversation_update.title
            if conversation_update.status:
                conversation.status = conversation_update.status
            return await self.service.update_conversation(conversation)
        return None

    async def delete_conversation(self, conversation_id: str) -> None:
        return await self.service.delete_conversation(conversation_id)
