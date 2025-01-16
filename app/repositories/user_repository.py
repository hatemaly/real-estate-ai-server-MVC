# src/repositories/user_repository.py
from pymongo.collection import Collection
from typing import List, Optional
from app.models.user_models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        document = await self.collection.find_one({"email": email})
        if document:
            return self.model(**document)
        return None

    async def get_users_by_role(self, role: str, skip: int = 0, limit: int = 50) -> List[User]:
        cursor = self.collection.find({"role": role}).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [self.model(**doc) for doc in documents]

    async def get_users_ids_by_role(self, role: str) -> List[str]:
        cursor = self.collection.find({"role": role}, {"_id": 1})
        return [doc["_id"] for doc in await cursor.to_list(length=None)]

    async def get_user_role_by_id(self, user_id: str) -> Optional[str]:
        document = await self.collection.find_one({"_id": user_id}, {"role": 1})
        return document["role"] if document else None
