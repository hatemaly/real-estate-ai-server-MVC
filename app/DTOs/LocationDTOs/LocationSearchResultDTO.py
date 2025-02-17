from typing import List, Optional
from pydantic import BaseModel

from app.DTOs.LocationDTOs.LocationResponseDTO import LocationResponseDTO


class LocationSearchResultDTO(BaseModel):
    items: List[LocationResponseDTO]
    total: int
    page: int
    limit: int
    pages: int
