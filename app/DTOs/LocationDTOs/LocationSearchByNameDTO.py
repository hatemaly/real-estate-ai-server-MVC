from pydantic import BaseModel
from typing import Optional


class LocationSearchByNameDTO(BaseModel):
    name: str
    exact_match: Optional[bool] = False
    page: Optional[int] = 1
    limit: Optional[int] = 10