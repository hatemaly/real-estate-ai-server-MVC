# app/models/developer_models/developer.py
from pydantic import  Field
from typing import Optional, List

from app.models.base_model import BaseModelApp
from app.models.developer_models.basic_info import DeveloperBasicInfo
from app.models.developer_models.detailed_info import DeveloperDetailedInfo
from app.models.developer_models.backend_info import DeveloperBackendInfo


class Developer(BaseModelApp):
    basic_info: DeveloperBasicInfo
    detailed_info: Optional[DeveloperDetailedInfo] = None
    backend_info: Optional[DeveloperBackendInfo] = None

    def update_basic_info(self, basic_info: DeveloperBasicInfo) -> None:
        """Update basic developer information."""
        self.basic_info = basic_info

    def update_detailed_info(self, detailed_info: DeveloperDetailedInfo) -> None:
        """Update detailed developer information."""
        self.detailed_info = detailed_info

    def update_backend_info(self, backend_info: DeveloperBackendInfo) -> None:
        """Update backend-specific developer information."""
        self.backend_info = backend_info
