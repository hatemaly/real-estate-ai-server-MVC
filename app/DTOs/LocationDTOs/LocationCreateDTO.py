from pydantic import BaseModel
from typing import List, Optional
from app.models.location_models.location import LocationType


class CoordinatesDTO(BaseModel):
    latitude: float
    longitude: float


class LocationCreateDTO(BaseModel):
    name: str
    other_names: List[str] = []
    location_type: List[LocationType] = []
    parent_ids: List[str] = []
    coordinates: CoordinatesDTO
    average_price_m2: Optional[float] = None
    gallery_urls: List[str] = []


class LocationUpdateDTO(LocationCreateDTO):
    name: Optional[str] = None
    other_names: Optional[List[str]] = None
    location_type: Optional[List[LocationType]] = None
    parent_ids: Optional[List[str]] = None
    coordinates: Optional[CoordinatesDTO] = None
    average_price_m2: Optional[float] = None
    gallery_urls: Optional[List[str]] = None
