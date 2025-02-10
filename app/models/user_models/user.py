from typing import List, Optional
from pydantic import  Field, EmailStr
from enum import Enum
from datetime import datetime

from app.models.base_model import BaseModelApp
from app.models.user_models.user_preferences import UserPreferences


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    AGENT = "agent"


class Language(str, Enum):
    EN = "en"
    AR = "ar"


class Email(BaseModelApp):
    address: EmailStr
    is_verified: bool = False


class Phone(BaseModelApp):
    number: str
    is_verified: bool = False


class User(BaseModelApp):
    email: Email
    password_hash: Optional[str] = None
    full_name: str
    phone: Optional[Phone] = None
    role: UserRole = UserRole.USER
    language: Language = Language.EN
    verification_code: Optional[str] = None
    reset_token: Optional[str] = None
    reset_token_expiry: Optional[datetime] = None
    # Here we changed the preferences field to a list of UserPreferences
    # preferences: List[UserPreferences] = Field(default_factory=list)

    favorites: List[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
