# src/models/user_models/user_preferences.py
from pydantic import  Field
from typing import List, Optional

from app.models.base_model import BaseModelApp


class PriceRange(BaseModelApp):
    min_price: Optional[float] = None
    max_price: Optional[float] = None


class UserPreferences():
    id: Optional[str] = Field(alias="_id")  # MongoDB's primary key
    preferred_locations: List[str] = Field(default_factory=list)
    preferred_property_types: List[str] = Field(default_factory=list)
    price_range: Optional[PriceRange] = None
