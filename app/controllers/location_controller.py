# src/controllers/location_controller.py
from typing import List
from app.services.location_service import LocationService
from app.models.location_models.location import Location, LocationType


class LocationController:
    def __init__(self, location_service: LocationService):
        self.location_service = location_service

    async def create_location(self, location: Location) -> Location:
        return await self.location_service.create_location(location)

    async def get_location_by_id(self, location_id: str) -> Location:
        return await self.location_service.get_location_by_id(location_id)

    async def get_locations_by_type(self, location_type: LocationType) -> List[Location]:
        return await self.location_service.get_locations_by_type(location_type)

    async def get_direct_children(self, location_id: str) -> List[Location]:
        return await self.location_service.get_direct_children(location_id)

    async def get_direct_parents(self, location_id: str) -> List[Location]:
        return await self.location_service.get_direct_parents(location_id)

    async def update_location(self, location: Location) -> Location:
        return await self.location_service.update_location(location)

    async def delete_location(self, location_id: str) -> None:
        await self.location_service.delete_location(location_id)
