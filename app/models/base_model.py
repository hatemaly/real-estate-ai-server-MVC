from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime


class BaseModelApp(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()