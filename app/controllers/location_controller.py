# src/controllers/location_controller.py
from fastapi import HTTPException

from app.DTOs.LocationDTOs.LocationCreateDTO import LocationUpdateDTO, LocationCreateDTO
from app.DTOs.LocationDTOs.LocationResponseDTO import LocationResponseDTO
from app.DTOs.LocationDTOs.LocationSearchByNameDTO import LocationSearchByNameDTO
from app.DTOs.LocationDTOs.LocationSearchByTypeDTO import LocationSearchByTypeDTO
from app.DTOs.LocationDTOs.LocationSearchResultDTO import LocationSearchResultDTO
from app.services.location_service import LocationService


class LocationController:
    def __init__(self, location_service: LocationService):
        self.location_service = location_service

    # Endpoint for searching locations by name
    async def search_locations_by_name(self, data: LocationSearchByNameDTO) -> LocationSearchResultDTO:
        return await self.location_service.search_locations_by_name(data)

    # Endpoint for searching locations by type
    async def search_locations_by_type(self, data: LocationSearchByTypeDTO) -> LocationSearchResultDTO:
        return await self.location_service.search_locations_by_type(data)

    async def create_location(self, location: LocationCreateDTO) -> LocationResponseDTO:
        return await self.location_service.create_location(location)

    # Get a location by ID
    async def get_location_by_id(self, location_id: str) -> LocationResponseDTO:
        location = await self.location_service.get_location_by_id(location_id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return location

    # Update an existing location
    async def update_location(self, location_id: str, location: LocationUpdateDTO) -> LocationResponseDTO:
        return await self.location_service.update_location(location_id, location)

    async def delete_location(self, location_id: str) -> None:
        await self.location_service.delete_location(location_id)

    # List locations with pagination and filters
    async def list_locations(
            self,
            location_type: str = None,
            parent_id: str = None,
            search: str = None,
            page: int = 1,
            limit: int = 10
    ) -> LocationSearchResultDTO:
        return await self.location_service.list_locations(location_type, parent_id, search, page, limit)