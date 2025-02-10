# src/models/developer_models/backend_info.py
from pydantic import  Field
from typing import List, Optional

from app.models.base_model import BaseModelApp
from app.models.developer_models.base_data import ContactInfo, PartnerStatus


class DeveloperBackendInfo(BaseModelApp):
    contact: Optional[ContactInfo] = None
    partnership_status: Optional[PartnerStatus] = None
    broker_employee_ids: List[str] = Field(default_factory=list)
