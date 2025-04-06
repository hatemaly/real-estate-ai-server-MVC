# src/models/property_models/property.py
from pydantic import  Field
from typing import List, Optional
from datetime import datetime

from app.agents.MessageFormatExtractionAgent import FinishingType
from app.models.base_model import BaseModelApp
from app.models.property_models.price import Price
from enum import Enum


class PropertyType(Enum):
    APARTMENT = "apartment"
    VILLA = "villa"
    OFFICE = "office"


class UsageType(Enum):
    COMMERCIAL = "commercial"
    RESIDENTIAL = "residential"
    INDUSTRIAL = "industrial"


class Amenity(Enum):
    POOL = "pool"
    GYM = "gym"
    PARKING = "parking"
    SECURITY = "security"
    OTHER = "other"


class InstallmentType(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class ViewType(Enum):
    SEA_VIEW = "sea view"
    CITY_VIEW = "city view"
    MOUNTAIN_VIEW = "mountain view"
    OTHER = "other"


class DeliveryType(Enum):
    FINISHED = "finished"
    SEMI_FINISHED = "semi finished"
    FURNISHED = "furnished"
    CORE_AND_SHELL = "core and shell"
    OTHER = "other"


class Property(BaseModelApp):
    title: str
    description: str | None = None
    is_developer_type: bool | None = None
    developer_type_id: str | None = None

    # Location details
    location_ids: List[str] = Field(default_factory=list)

    # Pricing information
    current_price: Price | None = None

    # Property type and usage
    property_type: PropertyType | None = None
    usage_type: UsageType | None = None

    # Physical characteristics of the property
    area: float | None = None
    garden_area: float | None = None
    roof_area: float | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    finishing_type: FinishingType | None = None

    # Delivery and media information
    delivery_date: datetime | None = None
    basic_images: List[str] = Field(default_factory=list)
    floor_plan_images: List[str] = Field(default_factory=list)


class DetailedPropertyDetails(Property):
    # Property location and structure details
    floor_number: int | None = None  # Current floor of the property
    total_building_floors: int | None = None  # Total number of floors in the building
    building_area: float | None = None  # Total area of the building
    land_area: float | None = None  # Total land area of the property

    # Amenities and features
    amenities: List[Amenity] = Field(default_factory=list)  # List of available amenities
    view_type: list[ViewType] = Field(default_factory=list)  # Types of views available from the property
    delivery_type: DeliveryType | None = None  # Type of delivery for the property
    number_of_parking_spaces: int | None = None  # Number of parking spaces available

    # Property features
    is_elevator: bool | None = None  # Indicates if the property has an elevator
    is_swimming_pool: bool | None = None  # Indicates if the property has a swimming pool
    is_gym: bool | None = None  # Indicates if the property has a gym
    is_security: bool | None = None  # Indicates if the property has security features
    is_maid_room: bool | None = None  # Indicates if there is a maid's room

    # Media and documentation
    property_documents: List[str] = Field(default_factory=list)  # List of property documents
    property_brochures: List[str] = Field(default_factory=list)  # List of property brochures
    property_videos: List[str] = Field(default_factory=list)  # List of property videos
    property_floor_plans: List[str] = Field(default_factory=list)  # List of property floor plans
    property_images: List[str] = Field(default_factory=list)  # List of property images

    # Additional information
    similar_properties: List[str] = Field(default_factory=list)  # List of similar properties
    detailed_description: str | None = None  # Detailed description of the property


class BackOfficePropertyDetails(DetailedPropertyDetails):
    # Property status flags
    is_active: bool | None = None
    is_featured: bool | None = None
    is_published: bool | None = None
    is_sold: bool | None = None
    is_rented: bool | None = None
    is_deleted: bool | None = None
    is_archived: bool | None = None

    # Owner information
    owner_id: str | None = None  # developer id
    owner_name: str | None = None
    owner_phone: str | None = None
    owner_email: str | None = None

    # Price and broker information
    price_history: List[Price] = Field(default_factory=list)
    broker_ids: List[str] = Field(default_factory=list)

