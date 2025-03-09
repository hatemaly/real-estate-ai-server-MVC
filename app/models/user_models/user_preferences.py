# src/models/user_models/user_preferences.py
from pydantic import Field
from typing import List, Optional
from pydantic import BaseModel

from app.models.property_models.property import Property


class PriceRange(BaseModel):
    min_price: Optional[float] = None
    max_price: Optional[float] = None


class UserPreferences(BaseModel):
    preferred_locations: List[str] = Field(default_factory=list)
    preferred_property_types: List[str] = Field(default_factory=list)
    preferred_properties: List[Property] = Field(default_factory=list)
    price_range: Optional[PriceRange] = None
