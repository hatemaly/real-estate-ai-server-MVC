# src/services/location_service.py
# This module contains the LocationService class which implements business logic
# for geographical location management. It handles CRUD operations for locations
# and specialized methods for working with location hierarchies.

from typing import List, Optional
from app.models.location_models.location import Location, LocationType
from app.repositories.location_repository import LocationRepository


class LocationService:
    """
    Service class for managing location-related business logic.
    
    This service provides methods for creating, retrieving, updating, and deleting locations,
    as well as specialized operations for working with location hierarchies and types.
    It delegates data access operations to the location repository.
    
    Attributes:
        repository: The repository that handles data access operations for locations
    """
    def __init__(self, repository: LocationRepository):
        """
        Initialize the location service with a repository.
        
        Args:
            repository: The repository that will handle data access operations
        """
        self.repository = repository

    async def create_location(self, location: Location) -> Location:
        """
        Create a new location.
        
        Args:
            location: The location data to save
            
        Returns:
            Location: The created location with assigned ID
        """
        await self.repository.save(location)
        return location

    async def update_location(self, location: Location) -> Location:
        """
        Update an existing location.
        
        Args:
            location: The location data to update (must include ID)
            
        Returns:
            Location: The updated location
            
        Raises:
            Exception: If location with the ID doesn't exist
        """
        await self.repository.update(location)
        return location

    async def delete_location(self, location_id: str) -> None:
        """
        Delete a location by ID.
        
        Args:
            location_id: The ID of the location to delete
            
        Raises:
            Exception: If location with the ID doesn't exist or has children
        """
        await self.repository.delete(location_id)

    async def get_location_by_id(self, location_id: str) -> Optional[Location]:
        """
        Get a location by its ID.
        
        Args:
            location_id: The ID of the location to retrieve
            
        Returns:
            Optional[Location]: The location if found, None otherwise
        """
        return await self.repository.get_by_id(location_id)

    async def get_locations_by_type(self, location_type: LocationType) -> List[Location]:
        """
        Get all locations of a specific type.
        
        Args:
            location_type: The location type to filter by (e.g., city, district)
            
        Returns:
            List[Location]: A list of locations with the specified type
        """
        return await self.repository.get_by_type(location_type)

    async def get_direct_children(self, location_id: str) -> List[Location]:
        """
        Get all direct child locations of a specified location.
        
        This retrieves locations that have the specified location as a direct parent.
        Used for navigating down the location hierarchy.
        
        Args:
            location_id: The ID of the parent location
            
        Returns:
            List[Location]: A list of child locations
        """
        return await self.repository.get_direct_children(location_id)

    async def get_direct_parents(self, location_id: str) -> List[Location]:
        """
        Get all direct parent locations of a specified location.
        
        This retrieves locations that are direct parents of the specified location.
        Used for navigating up the location hierarchy.
        
        Args:
            location_id: The ID of the child location
            
        Returns:
            List[Location]: A list of parent locations
        """
        return await self.repository.get_direct_parents(location_id)
