# src/services/location_service.py
from typing import List, Optional
from app.models.location_models.location import Location, LocationType
from app.repositories.location_repository import LocationRepository


class LocationService:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def create_location(self, location: Location) -> Location:
        await self.repository.save(location)
        return location

    async def update_location(self, location: Location) -> Location:
        await self.repository.update(location)
        return location

    async def delete_location(self, location_id: str) -> None:
        await self.repository.delete(location_id)

    async def get_location_by_id(self, location_id: str) -> Optional[Location]:
        return await self.repository.get_by_id(location_id)

    async def get_locations_by_type(self, location_type: LocationType) -> List[Location]:
        return await self.repository.get_by_type(location_type)

    async def get_direct_children(self, location_id: str) -> List[Location]:
        return await self.repository.get_direct_children(location_id)

    async def get_direct_parents(self, location_id: str) -> List[Location]:
        return await self.repository.get_direct_parents(location_id)
