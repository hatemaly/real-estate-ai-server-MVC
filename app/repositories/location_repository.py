# src/repositories/location_repository.py
from pymongo.collection import Collection
from typing import List

from app.DTOs.LocationDTOs.LocationCreateDTO import LocationCreateDTO, LocationUpdateDTO
from app.models.location_models.location import Location, LocationType
from app.repositories.base_repository import BaseRepository


class LocationRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, Location)

    # Existing methods...

    async def search_by_name(self, name: str, exact_match: bool = False, page: int = 1, limit: int = 10) -> List[Location]:
        query = {"name": name} if exact_match else {"name": {"$regex": name, "$options": "i"}}
        cursor = self.collection.find(query).skip((page - 1) * limit).limit(limit)
        documents = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in documents]

    async def count_by_name(self, name: str, exact_match: bool = False) -> int:
        query = {"name": name} if exact_match else {"name": {"$regex": name, "$options": "i"}}
        count = await self.collection.count_documents(query)
        return count

    async def search_by_type(self, location_type: LocationType, page: int = 1, limit: int = 10) -> List[Location]:
        cursor = self.collection.find({"location_type": location_type}).skip((page - 1) * limit).limit(limit)
        documents = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in documents]

    async def count_by_type(self, location_type: LocationType) -> int:
        count = await self.collection.count_documents({"location_type": location_type})
        return count

    async def create(self, location: LocationCreateDTO) -> Location:
        document = location.dict(by_alias=True)
        result = await self.collection.insert_one(document)
        return await self.get_by_id(str(result.inserted_id))

    # Get location by ID
    async def get_by_id(self, location_id: str) -> Location:
        document = await self.collection.find_one({"_id": location_id})
        if document:
            return self.model(**document)
        return None

    # Update location
    async def update(self, location_id: str, location: LocationUpdateDTO) -> Location:
        document = location.dict(exclude_unset=True, by_alias=True)
        await self.collection.update_one({"_id": location_id}, {"$set": document})
        return await self.get_by_id(location_id)

    async def delete(self, location_id: str) -> None:
        await self.collection.delete_one({"_id": location_id})

    # List locations with filters, pagination, and search
    async def list_locations(
            self,
            location_type: str = None,
            parent_id: str = None,
            search: str = None,
            page: int = 1,
            limit: int = 10
    ) -> List[Location]:
        query = {}

        if location_type:
            query["location_type"] = location_type
        if parent_id:
            query["parent_ids"] = parent_id
        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        cursor = self.collection.find(query).skip((page - 1) * limit).limit(limit)
        documents = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in documents]

    async def count_locations(
            self,
            location_type: str = None,
            parent_id: str = None,
            search: str = None
    ) -> int:
        query = {}

        if location_type:
            query["location_type"] = location_type
        if parent_id:
            query["parent_ids"] = parent_id
        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        count = await self.collection.count_documents(query)
        return count
