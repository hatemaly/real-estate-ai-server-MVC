# src/repositories/property_repository.py
from pymongo.collection import Collection
from typing import List, Optional
from app.models.property_models.property import Property
from app.repositories.base_repository import BaseRepository


class PropertyRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, Property)

    async def get_all_ids(self) -> List[str]:
        cursor = self.collection.find({}, {"_id": 1})
        return [doc["_id"] for doc in await cursor.to_list(length=None)]

    async def get_active_properties_ids(self) -> List[str]:
        cursor = self.collection.find({"is_active": True}, {"_id": 1})
        return [doc["_id"] for doc in await cursor.to_list(length=None)]
