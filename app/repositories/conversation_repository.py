# app/repositories/conversation_repository.py
from pymongo.collection import Collection
from typing import List
from app.models.conversation_models.conversation import Conversation
from app.repositories.base_repository import BaseRepository


class ConversationRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, Conversation)

    async def retrieve_conversation_history_by_id(self, conversation_id: str, limit: int = 10, offset: int = 0) -> Conversation:
        document = await self.collection.find_one({"_id": conversation_id})
        if document:
            return self.model(**document)
        return None

    async def retrieve_conversation_info_by_user_id(self, user_id: str) -> List[Conversation]:
        cursor = self.collection.find({"user_id": user_id})
        documents = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in documents]