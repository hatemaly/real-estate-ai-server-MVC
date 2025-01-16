# src/models/developer_models/base_data.py
from pydantic import BaseModel
from enum import Enum
from typing import Optional


class ProjectStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


class Specialization(str, Enum):
    COMMERCIAL = "commercial"
    ADMINISTRATIVE = "administrative"
    RESIDENTIAL = "residential"
    INDUSTRIAL = "industrial"
    MEDICAL = "medical"
    OTHER = "other"


class PartnerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ProjectWithStatus(BaseModel):
    project_name: str
    status: ProjectStatus


class ContactInfo(BaseModel):
    person: str
    email: str
    phone: str
