# src/models/developer_models/base_data.py
from enum import Enum
from typing import Optional

from app.models.base_model import BaseModelApp


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


class ProjectWithStatus(BaseModelApp):
    project_name: str
    status: ProjectStatus


class ContactInfo(BaseModelApp):
    person: str
    email: str
    phone: str
