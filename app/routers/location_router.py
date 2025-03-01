# app/routers/location_router.py
from fastapi import APIRouter, Depends
from typing import List, Optional

from app.DTOs.LocationDTOs.GalleryUpdateDTO import GalleryUpdateRequestDTO, GalleryUpdateResponseDTO
from app.DTOs.LocationDTOs.LocationCreateDTO import LocationUpdateDTO, LocationCreateDTO
from app.DTOs.LocationDTOs.LocationParentsResponseDTO import LocationParentsResponseDTO
from app.DTOs.LocationDTOs.LocationResponseDTO import LocationResponseDTO
from app.DTOs.LocationDTOs.LocationSearchByNameDTO import LocationSearchByNameDTO
from app.DTOs.LocationDTOs.LocationSearchByTypeDTO import LocationSearchByTypeDTO
from app.DTOs.LocationDTOs.LocationSearchResultDTO import LocationSearchResultDTO
from app.DTOs.LocationDTOs.PriceUpdateDTO import PriceUpdateRequestDTO, PriceUpdateResponseDTO
from app.controllers.location_controller import LocationController
from app.repositories.location_repository import LocationRepository
from app.database.collections import get_location_collection
from app.services.location_service import LocationService
from app.models.location_models.location import Location, LocationType

router = APIRouter()
# src/routers/location_router.py
from fastapi import APIRouter, Depends
from app.controllers.location_controller import LocationController
from app.services.location_service import LocationService
from app.repositories.location_repository import LocationRepository
from app.database.collections import get_location_collection

router = APIRouter()

# Dependency to get the location controller
async def get_location_controller() -> LocationController:
    location_collection = await get_location_collection()
    repository = LocationRepository(location_collection)
    service = LocationService(repository)
    return LocationController(service)

# Search locations by name
@router.get("/search/name", response_model=LocationSearchResultDTO)
async def search_locations_by_name(
    name: str,
    exact_match: bool = False,
    page: int = 1,
    limit: int = 10,
    controller: LocationController = Depends(get_location_controller)
):
    search_data = LocationSearchByNameDTO(name=name, exact_match=exact_match, page=page, limit=limit)
    return await controller.search_locations_by_name(search_data)

# Search locations by type
@router.get("/search/type", response_model=LocationSearchResultDTO)
async def search_locations_by_type(
    location_type: str,
    page: int = 1,
    limit: int = 10,
    controller: LocationController = Depends(get_location_controller)
):
    search_data = LocationSearchByTypeDTO(location_type=location_type, page=page, limit=limit)
    return await controller.search_locations_by_type(search_data)

@router.post("/", response_model=LocationResponseDTO)
async def create_location(location: LocationCreateDTO, controller: LocationController = Depends(get_location_controller)):
    return await controller.create_location(location)

# Get a location by ID
@router.get("/{location_id}", response_model=LocationResponseDTO)
async def get_location(location_id: str, controller: LocationController = Depends(get_location_controller)):
    return await controller.get_location_by_id(location_id)

# Update an existing location
@router.put("/{location_id}", response_model=LocationResponseDTO)
async def update_location(location_id: str, location: LocationUpdateDTO, controller: LocationController = Depends(get_location_controller)):
    return await controller.update_location(location_id, location)

@router.delete("/{location_id}", status_code=204)
async def delete_location(location_id: str, controller: LocationController = Depends(get_location_controller)):
    await controller.delete_location(location_id)

# List locations with pagination and filters
@router.get("/", response_model=LocationSearchResultDTO)
async def list_locations(
    location_type: str = None,
    parent_id: str = None,
    search: str = None,
    page: int = 1,
    limit: int = 10,
    controller: LocationController = Depends(get_location_controller)
):
    return await controller.list_locations(location_type, parent_id, search, page, limit)


@router.get("/{location_id}/children", response_model=LocationSearchResultDTO)
async def get_children(
    location_id: str,
    page: int = 1,
    limit: int = 10,
    location_type: Optional[str] = None,
    controller: LocationController = Depends(get_location_controller)
):
    return await controller.get_location_children(location_id, page, limit, location_type)

@router.get("/{location_id}/parents", response_model=LocationParentsResponseDTO)
async def get_parents(
    location_id: str,
    location_type: Optional[str] = None,
    controller: LocationController = Depends(get_location_controller)
):
    return await controller.get_location_parents(location_id, location_type)

@router.put("/{location_id}/gallery", response_model=GalleryUpdateResponseDTO)
async def update_gallery(
    location_id: str,
    data: GalleryUpdateRequestDTO,
    controller: LocationController = Depends(get_location_controller)
):
    return await controller.update_location_gallery(location_id, data)

@router.put("/{location_id}/price", response_model=PriceUpdateResponseDTO)
async def update_price(
    location_id: str,
    data: PriceUpdateRequestDTO,
    controller: LocationController = Depends(get_location_controller)
):
    return await controller.update_location_price(location_id, data)