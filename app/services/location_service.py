# src/services/location_service.py
from typing import Optional

from fastapi import HTTPException

from app.DTOs.LocationDTOs.GalleryUpdateDTO import GalleryUpdateResponseDTO
from app.DTOs.LocationDTOs.LocationCreateDTO import LocationUpdateDTO, LocationCreateDTO
from app.DTOs.LocationDTOs.LocationParentsResponseDTO import LocationParentsResponseDTO
from app.DTOs.LocationDTOs.LocationResponseDTO import LocationResponseDTO
from app.DTOs.LocationDTOs.LocationSearchByNameDTO import LocationSearchByNameDTO
from app.DTOs.LocationDTOs.LocationSearchByTypeDTO import LocationSearchByTypeDTO
from app.DTOs.LocationDTOs.LocationSearchResultDTO import LocationSearchResultDTO
from app.DTOs.LocationDTOs.PriceUpdateDTO import PriceUpdateResponseDTO
from app.repositories.location_repository import LocationRepository


class LocationService:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def search_locations_by_name(self, data: LocationSearchByNameDTO) -> LocationSearchResultDTO:
        locations = await self.repo.search_by_name(data.name, data.exact_match, data.page, data.limit)
        total = await self.repo.count_by_name(data.name, data.exact_match)
        pages = (total // data.limit) + (1 if total % data.limit > 0 else 0)

        # Create LocationResponseDTO from Location objects
        result = LocationSearchResultDTO(
            items=[LocationResponseDTO.from_orm(location) for location in locations],
            total=total,
            page=data.page,
            limit=data.limit,
            pages=pages
        )
        return result

    async def search_locations_by_type(self, data: LocationSearchByTypeDTO) -> LocationSearchResultDTO:
        locations = await self.repo.search_by_type(data.location_type, data.page, data.limit)
        total = await self.repo.count_by_type(data.location_type)
        pages = (total // data.limit) + (1 if total % data.limit > 0 else 0)

        # Create LocationResponseDTO from Location objects
        result = LocationSearchResultDTO(
            items=[LocationResponseDTO.from_orm(location) for location in locations],
            total=total,
            page=data.page,
            limit=data.limit,
            pages=pages
        )
        return result

    async def create_location(self, data: LocationCreateDTO) -> LocationResponseDTO:
        # Create the location in the repository
        created_location = await self.repo.create(data)

        # Return the created location as a DTO
        return LocationResponseDTO.from_orm(created_location)

        # Get Location by ID

    async def get_location_by_id(self, location_id: str) -> LocationResponseDTO:
        location = await self.repo.get_by_id(location_id)
        if not location:
            raise ValueError("Location not found")

        # Return the location data as DTO
        return LocationResponseDTO.from_orm(location)

        # Update Location

    async def update_location(self, location_id: str, data: LocationUpdateDTO) -> LocationResponseDTO:
        updated_location = await self.repo.update(location_id, data)
        return LocationResponseDTO.from_orm(updated_location)

    async def delete_location(self, location_id: str) -> None:
        await self.repo.delete(location_id)

    # List Locations
    async def list_locations(
            self,
            location_type: str = None,
            parent_id: str = None,
            search: str = None,
            page: int = 1,
            limit: int = 10
    ) -> LocationSearchResultDTO:
        locations = await self.repo.list_locations(location_type, parent_id, search, page, limit)
        total = await self.repo.count_locations(location_type, parent_id, search)
        pages = (total // limit) + (1 if total % limit > 0 else 0)

        return LocationSearchResultDTO(
            items=[LocationResponseDTO.from_orm(location) for location in locations],
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )

    async def get_location_children(
            self,
            location_id: str,
            page: int,
            limit: int,
            location_type: Optional[str] = None
    ) -> LocationSearchResultDTO:
        items = await self.repository.list_locations(
            location_type=location_type,
            parent_id=location_id,
            page=page,
            limit=limit
        )
        total = await self.repository.count_locations(
            location_type=location_type,
            parent_id=location_id
        )
        pages = (total + limit - 1) // limit
        return LocationSearchResultDTO(
            items=[self._convert_to_dto(item) for item in items],
            total=total,
            page=page,
            pages=pages
        )

    async def get_location_parents(
            self,
            location_id: str,
            location_type: Optional[str] = None
    ) -> LocationParentsResponseDTO:
        location = await self.repository.get_by_id(location_id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        parent_ids = location.parent_ids
        parents = await self.repository.get_by_ids(parent_ids) if parent_ids else []
        if location_type:
            parents = [p for p in parents if p.location_type == location_type]
        return LocationParentsResponseDTO(items=[self._convert_to_dto(p) for p in parents])

    async def update_gallery(
            self,
            location_id: str,
            gallery_urls: list[str]
    ) -> GalleryUpdateResponseDTO:
        update_data = LocationUpdateDTO(gallery_urls=gallery_urls)
        updated = await self.repository.update(location_id, update_data)
        return GalleryUpdateResponseDTO(gallery_urls=updated.gallery_urls)

    async def update_price(
            self,
            location_id: str,
            average_price_m2: float
    ) -> PriceUpdateResponseDTO:
        update_data = LocationUpdateDTO(average_price_m2=average_price_m2)
        updated = await self.repository.update(location_id, update_data)
        return PriceUpdateResponseDTO(average_price_m2=updated.average_price_m2)
