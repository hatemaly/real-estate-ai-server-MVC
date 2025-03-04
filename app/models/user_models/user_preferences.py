# src/models/user_models/user_preferences.py
# This module defines models for storing user preferences related to real estate searches.
# It includes preferences for locations, property types, and price ranges.

from pydantic import BaseModel, Field
from typing import List, Optional


class PriceRange(BaseModel):
    """
    Model representing a user's preferred price range for properties.
    
    Attributes:
        min_price: The minimum price the user is willing to pay (optional)
        max_price: The maximum price the user is willing to pay (optional)
    """
    min_price: Optional[float] = None  # Minimum price user is willing to pay
    max_price: Optional[float] = None  # Maximum price user is willing to pay


class UserPreferences(BaseModel):
    """
    Model storing all user preferences for property searches.
    
    Attributes:
        id: Unique identifier for the preferences record, uses MongoDB's ObjectId
        preferred_locations: List of location identifiers the user is interested in
        preferred_property_types: List of property types the user is interested in
        price_range: The user's preferred price range for properties
    """
    id: Optional[str] = Field(alias="_id")  # MongoDB's primary key
    preferred_locations: List[str] = Field(default_factory=list)  # List of preferred location IDs
    preferred_property_types: List[str] = Field(default_factory=list)  # List of preferred property types
    price_range: Optional[PriceRange] = None  # User's preferred price range
