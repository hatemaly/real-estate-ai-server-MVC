# app/routers/location_router.py
# This module defines the FastAPI router for location-related API endpoints.
# It sets up routes for CRUD operations on location resources, as well as
# specialized endpoints for location hierarchy management (parents/children).

from fastapi import APIRouter, Depends
from typing import List
from app.controllers.location_controller import LocationController
from app.repositories.location_repository import LocationRepository
from app.database.collections import get_location_collection
from app.services.location_service import LocationService
from app.models.location_models.location import Location, LocationType

# Create an API router for location endpoints
router = APIRouter()

async def get_location_controller() -> LocationController:
    """
    Dependency injection function to create and provide a LocationController instance.
    
    This function follows the repository pattern, creating the entire dependency chain:
    database collection -> repository -> service -> controller
    
    Returns:
        LocationController: A configured controller for handling location operations
    """
    location_collection = await get_location_collection()
    repository = LocationRepository(location_collection)
    service = LocationService(repository)
    return LocationController(service)

@router.post("/", response_model=Location)
async def create_location(location: Location, controller: LocationController = Depends(get_location_controller)):
    """
    Create a new location.
    
    Args:
        location: Location data from request body
        controller: LocationController instance (injected dependency)
    
    Returns:
        Location: The created location with assigned ID
    """
    return await controller.create_location(location)

@router.get("/{location_id}", response_model=Location)
async def get_location(location_id: str, controller: LocationController = Depends(get_location_controller)):
    """
    Get a location by its ID.
    
    Args:
        location_id: The unique identifier of the location to retrieve
        controller: LocationController instance (injected dependency)
    
    Returns:
        Location: The location with the specified ID
        
    Raises:
        HTTPException: If no location with the given ID exists
    """
    return await controller.get_location_by_id(location_id)

@router.get("/type/{location_type}", response_model=List[Location])
async def get_locations_by_type(location_type: LocationType, controller: LocationController = Depends(get_location_controller)):
    """
    Get a list of locations with a specific type.
    
    Args:
        location_type: The location type to filter by (e.g., city, district, neighborhood)
        controller: LocationController instance (injected dependency)
    
    Returns:
        List[Location]: A list of locations with the specified type
    """
    return await controller.get_locations_by_type(location_type)

@router.get("/{location_id}/children", response_model=List[Location])
async def get_direct_children(location_id: str, controller: LocationController = Depends(get_location_controller)):
    """
    Get all direct child locations of a specified location.
    
    This retrieves locations that have the specified location as a direct parent,
    allowing navigation down the location hierarchy.
    
    Args:
        location_id: The unique identifier of the parent location
        controller: LocationController instance (injected dependency)
    
    Returns:
        List[Location]: A list of child locations
        
    Raises:
        HTTPException: If no location with the given ID exists
    """
    return await controller.get_direct_children(location_id)

@router.get("/{location_id}/parents", response_model=List[Location])
async def get_direct_parents(location_id: str, controller: LocationController = Depends(get_location_controller)):
    """
    Get all direct parent locations of a specified location.
    
    This retrieves locations that are direct parents of the specified location,
    allowing navigation up the location hierarchy.
    
    Args:
        location_id: The unique identifier of the child location
        controller: LocationController instance (injected dependency)
    
    Returns:
        List[Location]: A list of parent locations
        
    Raises:
        HTTPException: If no location with the given ID exists
    """
    return await controller.get_direct_parents(location_id)

@router.put("/", response_model=Location)
async def update_location(location: Location, controller: LocationController = Depends(get_location_controller)):
    """
    Update an existing location.
    
    Args:
        location: Updated location data from request body (must include ID)
        controller: LocationController instance (injected dependency)
    
    Returns:
        Location: The updated location
        
    Raises:
        HTTPException: If no location with the given ID exists
    """
    return await controller.update_location(location)

@router.delete("/{location_id}")
async def delete_location(location_id: str, controller: LocationController = Depends(get_location_controller)):
    """
    Delete a location by its ID.
    
    Args:
        location_id: The unique identifier of the location to delete
        controller: LocationController instance (injected dependency)
    
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If no location with the given ID exists or if the location
                     has child locations that would become orphaned
    """
    await controller.delete_location(location_id)
    return {"message": "Location deleted successfully"}
