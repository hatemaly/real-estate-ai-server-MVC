# app/DTOs/LocationDTOs/LocationUpdateDTO.py
from typing import Optional, List

from pydantic import BaseModel

from app.models.location_models.location import LocationType, Coordinates

class LocationUpdateDTO(BaseModel):
    name: Optional[str] = None
    location_type: Optional[LocationType] = None
    coordinates: Optional[Coordinates] = None
    parent_ids: Optional[List[str]] = None
    gallery_urls: Optional[List[str]] = None
    average_price_m2: Optional[float] = None