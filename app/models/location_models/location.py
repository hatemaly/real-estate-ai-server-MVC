# src/models/location_models/location.py
# This module defines models for handling geographical locations in the real estate application.
# It includes location types, geographical coordinates, and location metadata.

from enum import Enum

from pydantic import BaseModel, Field
from typing import List, Optional


class LocationType(str, Enum):
    """
    Enumeration of location types for hierarchical location organization.
    
    These types form a hierarchy from broadest (governorate) to most specific (building),
    allowing for flexible location searching and filtering.
    
    Values:
        GOVERNORATE: Largest administrative division (like a state or province)
        CITY: Large urban area within a governorate
        DISTRICT: Division within a city
        NEIGHBORHOOD: Smaller division within a district
        STREET: Named street within a neighborhood
        BUILDING: Specific building on a street
        POINT_OF_INTEREST: Notable location (landmark, park, etc.)
        OTHER: Any other type of location not covered above
    """
    GOVERNORATE = "governorate"  # Largest administrative division
    CITY = "city"  # Large urban area
    DISTRICT = "district"  # Subdivision of a city
    NEIGHBORHOOD = "neighborhood"  # Subdivision of a district
    STREET = "street"  # Named street
    BUILDING = "building"  # Specific building
    POINT_OF_INTEREST = "point_of_interest"  # Landmark or notable location
    OTHER = "other"  # Miscellaneous location type


class Coordinates(BaseModel):
    """
    Model for storing geographical coordinates.
    
    These coordinates can be used for mapping and distance calculations.
    
    Attributes:
        latitude: North-south position (degrees)
        longitude: East-west position (degrees)
    """
    latitude: float  # North-south position in degrees
    longitude: float  # East-west position in degrees


class Location(BaseModel):
    """
    Model representing a geographical location in the real estate system.
    
    This model contains information about a specific location, including its type,
    position in the location hierarchy, coordinates, and real estate market data.
    
    Attributes:
        id: Unique identifier for the location
        name: Name of the location
        location_type: Type of location in the hierarchy
        parent_ids: IDs of parent locations (for hierarchical navigation)
        coordinates: Geographical coordinates (optional)
        average_price_m2: Average property price per square meter in this location (optional)
        gallery_urls: List of image URLs showing this location (optional)
    """
    id: Optional[str] = None  # Unique location identifier
    name: str  # Location name
    location_type: LocationType  # Type of location in hierarchy
    parent_ids: List[str] = Field(default_factory=list)  # IDs of parent locations
    coordinates: Optional[Coordinates] = None  # Geographical coordinates
    average_price_m2: Optional[float] = None  # Average price per square meter
    gallery_urls: List[str] = Field(default_factory=list)  # Image URLs of this location
