# app/routers/location_router.py
from fastapi import APIRouter, Depends
from typing import List
from app.controllers.location_controller import LocationController
from app.repositories.location_repository import LocationRepository
from app.database.collections import get_location_collection
from app.services.location_service import LocationService
from app.models.location_models.location import Location, LocationType

router = APIRouter()

async def get_location_controller() -> LocationController:
    location_collection = await get_location_collection()
    repository = LocationRepository(location_collection)
    service = LocationService(repository)
    return LocationController(service)

@router.post("/", response_model=Location)
async def create_location(location: Location, controller: LocationController = Depends(get_location_controller)):
    return await controller.create_location(location)

@router.get("/{location_id}", response_model=Location)
async def get_location(location_id: str, controller: LocationController = Depends(get_location_controller)):
    return await controller.get_location_by_id(location_id)

@router.get("/type/{location_type}", response_model=List[Location])
async def get_locations_by_type(location_type: LocationType, controller: LocationController = Depends(get_location_controller)):
    return await controller.get_locations_by_type(location_type)

@router.get("/{location_id}/children", response_model=List[Location])
async def get_direct_children(location_id: str, controller: LocationController = Depends(get_location_controller)):
    return await controller.get_direct_children(location_id)

@router.get("/{location_id}/parents", response_model=List[Location])
async def get_direct_parents(location_id: str, controller: LocationController = Depends(get_location_controller)):
    return await controller.get_direct_parents(location_id)

@router.put("/", response_model=Location)
async def update_location(location: Location, controller: LocationController = Depends(get_location_controller)):
    return await controller.update_location(location)

@router.delete("/{location_id}")
async def delete_location(location_id: str, controller: LocationController = Depends(get_location_controller)):
    await controller.delete_location(location_id)
    return {"message": "Location deleted successfully"}
