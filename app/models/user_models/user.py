from typing import List, Optional
from pydantic import  Field, EmailStr
from enum import Enum
from datetime import datetime

from app.models.base_model import BaseModelApp
from app.models.user_models.object_values import Email, Phone, UserRole, Language
from app.models.user_models.appointment_request import AppointmentRequest

class User(BaseModelApp):
    email: Email
    password_hash: Optional[str] = None
    first_name: str
    last_name: str
    phone: Optional[Phone] = None
    role: UserRole = UserRole.USER
    language: Language = Language.EN
    verification_code: Optional[str] = None
    reset_token: Optional[str] = None
    reset_token_expiry: Optional[datetime] = None
    favorites: List[str] = Field(default_factory=list)
    appointments: List[AppointmentRequest] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
