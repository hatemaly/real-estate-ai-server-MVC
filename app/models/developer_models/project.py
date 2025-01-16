# src/models/developer_models/project.py
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# Enums
class ProjectType(str, Enum):
    PHASE = "phase"
    PROJECT = "project"


class ProjectStatus(str, Enum):
    UNDER_CONSTRUCTION = "under_construction"
    COMPLETED = "completed"
    UPCOMING = "upcoming"


class ProjectUsage(str, Enum):
    COMMERCIAL = "commercial"
    RESIDENTIAL = "residential"
    INDUSTRIAL = "industrial"
    MIXED_USE = "mixed-use"


class Amenity(str, Enum):
    POOL = "pool"
    GYM = "gym"
    PARKING = "parking"
    SECURITY = "security"
    OTHER = "other"


class Feature(str, Enum):
    pass


class UnitType(str, Enum):
    STANDALONE = "standalone"
    APARTMENT = "apartment"
    CONDO = "condo"
    HOUSE = "house"
    OTHER = "other"


# Value Objects
class BackendProjectInfo(BaseModel):
    broker_employee_ids: List[str] = Field(default_factory=list)


class BasicProjectInfo(BaseModel):
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    parent_project_id: Optional[str] = None
    project_type: ProjectType = ProjectType.PROJECT
    status: ProjectStatus = ProjectStatus.UPCOMING
    delivery_date: Optional[datetime] = None
    starting_price: Optional[float] = None
    usage_types: List[ProjectUsage] = Field(default_factory=list)
    developer_ids: List[str] = Field(default_factory=list)


class DetailedProjectInfo(BaseModel):
    full_description: Optional[str] = None
    completion_date: Optional[datetime] = None
    available_units_count: Optional[int] = None
    available_unit_types: List[UnitType] = Field(default_factory=list)
    master_plan_urls: List[str] = Field(default_factory=list)
    image_urls: List[str] = Field(default_factory=list)
    document_urls: List[str] = Field(default_factory=list)
    video_urls: List[str] = Field(default_factory=list)
    amenities: List[Amenity] = Field(default_factory=list)
    features: List[Feature] = Field(default_factory=list)
    location_ids: List[str] = Field(default_factory=list)


# Project Entity
class Project(BaseModel):
    id: Optional[str] = None  # MongoDB or UUID
    basic_info: BasicProjectInfo
    detailed_info: Optional[DetailedProjectInfo] = None
    backend_info: Optional[BackendProjectInfo] = None

    def update_basic_info(self, basic_info: BasicProjectInfo) -> None:
        self.basic_info = basic_info

    def update_detailed_info(self, detailed_info: DetailedProjectInfo) -> None:
        self.detailed_info = detailed_info

    def update_backend_info(self, backend_info: BackendProjectInfo) -> None:
        self.backend_info = backend_info

    def add_broker_employee(self, employee_id: str) -> None:
        if self.backend_info and employee_id not in self.backend_info.broker_employee_ids:
            self.backend_info.broker_employee_ids.append(employee_id)

    def remove_broker_employee(self, employee_id: str) -> None:
        if self.backend_info and employee_id in self.backend_info.broker_employee_ids:
            self.backend_info.broker_employee_ids.remove(employee_id)
