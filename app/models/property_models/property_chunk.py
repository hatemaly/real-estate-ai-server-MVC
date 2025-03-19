from pydantic import  Field, BaseModel
from typing import List, Optional
from datetime import datetime

from app.models.base_model import BaseModelApp
from app.models.property_models.price import Price
from enum import Enum



class PropertyChunk(BaseModel):
    title: str
    description: Optional[str] = None