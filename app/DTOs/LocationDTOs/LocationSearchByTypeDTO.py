from pydantic import BaseModel
from typing import Optional
from app.models.location_models.location import LocationType


class LocationSearchByTypeDTO(BaseModel):
    location_type: LocationType
    page: Optional[int] = 1
    limit: Optional[int] = 10
