# src/models/location_models/location.py
from enum import Enum

from pydantic import BaseModel, Field
from typing import List, Optional


class LocationType(str, Enum):
    GOVERNORATE = "governorate"
    CITY = "city"
    DISTRICT = "district"
    NEIGHBORHOOD = "neighborhood"
    STREET = "street"
    BUILDING = "building"
    POINT_OF_INTEREST = "point_of_interest"
    OTHER = "other"


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class Location(BaseModel):
    id: Optional[str] = None
    name: str
    location_type: LocationType
    parent_ids: List[str] = Field(default_factory=list)
    coordinates: Optional[Coordinates] = None
    average_price_m2: Optional[float] = None
    gallery_urls: List[str] = Field(default_factory=list)
