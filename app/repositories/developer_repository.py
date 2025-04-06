# src/repositories/developer_repository.py
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection
from typing import List, Optional
from app.models.developer_models.developer import Developer
from app.repositories.base_repository import BaseRepository


class DeveloperRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, Developer)

    async def get_by_id(self, developer_id: str) -> Optional[Developer]:
        document = await self.collection.find_one({"_id": developer_id})
        if document:
            return self.model(**document)
        return None

    async def get_developers_by_ids(self, developer_ids: List[str]) -> List[Developer]:
        """
        Get multiple developers by list of IDs with proper error handling
        """
        valid_ids = []
        for dev_id in developer_ids:
            try:
                valid_ids.append(ObjectId(dev_id))
            except InvalidId:
                continue

        if not valid_ids:
            return []

    async def get_all(self) -> List[Developer]:
        cursor = self.collection.find({})
        documents = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in documents]
