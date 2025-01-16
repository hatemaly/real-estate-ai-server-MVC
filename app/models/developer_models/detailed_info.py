# src/models/developer_models/detailed_info.py
from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.developer_models.base_data import ProjectWithStatus, Specialization


class DeveloperDetailedInfo(BaseModel):
    name: str
    description: Optional[str] = None
    projects: Optional[List[ProjectWithStatus]] = None
    specializations: Optional[List[Specialization]] = None
    awards: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
