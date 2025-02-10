# src/models/developer_models/basic_info.py
from pydantic import  Field
from typing import Optional, List

from app.models.base_model import BaseModelApp


class DeveloperBasicInfo(BaseModelApp):
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    year_founded: Optional[int] = None
    total_projects: Optional[int] = None
    images: List[str] = Field(default_factory=list)
