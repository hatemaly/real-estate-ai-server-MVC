# src/repositories/location_repository.py
from pymongo.collection import Collection
from typing import List
from app.models.location_models.location import Location, LocationType
from app.repositories.base_repository import BaseRepository


class LocationRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, Location)

    async def get_by_type(self, location_type: LocationType) -> List[Location]:
        cursor = self.collection.find({"location_type": location_type})
        documents = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in documents]

    async def get_direct_children(self, location_id: str) -> List[Location]:
        cursor = self.collection.find({"parent_ids": location_id})
        documents = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in documents]
