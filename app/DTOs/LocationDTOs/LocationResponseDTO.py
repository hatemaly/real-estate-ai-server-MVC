from pydantic import BaseModel
from typing import List, Optional
from app.models.location_models.location import LocationType


class CoordinatesDTO(BaseModel):
    latitude: float
    longitude: float


class LocationResponseDTO(BaseModel):
    id: str
    name: str
    other_names: List[str]
    location_type: List[LocationType]
    parent_ids: List[str]
    coordinates: CoordinatesDTO
    average_price_m2: Optional[float]
    gallery_urls: List[str]
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
