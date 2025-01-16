# src/models/property_models/property.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.property_models.price import Price
from enum import Enum


class PropertyType(str, Enum):
    APARTMENT = "apartment"
    VILLA = "villa"
    OFFICE = "office"


class UsageType(str, Enum):
    COMMERCIAL = "commercial"
    RESIDENTIAL = "residential"
    INDUSTRIAL = "industrial"


class FinishingType(str, Enum):
    FINISHED = "finished"
    SEMI_FINISHED = "semi_finished"
    UNFINISHED = "unfinished"


class Property(BaseModel):
    id: Optional[str] = None  # MongoDB or UUID
    title: str
    description: Optional[str] = None
    location_ids: List[str] = Field(default_factory=list)
    property_type: PropertyType
    usage_type: UsageType
    area: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    finishing_type: Optional[FinishingType] = None
    delivery_date: Optional[datetime] = None
    basic_images: List[str] = Field(default_factory=list)
    floor_plan_images: List[str] = Field(default_factory=list)
    prices: List[Price] = Field(default_factory=list)  # List of price objects
    current_price: Optional[Price] = None
    is_active: bool = True
