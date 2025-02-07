from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime

from app.models.user_models.user_preferences import UserPreferences


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    AGENT = "agent"


class Language(str, Enum):
    EN = "en"
    AR = "ar"


class Email(BaseModel):
    address: EmailStr
    is_verified: bool = False


class Phone(BaseModel):
    number: str
    is_verified: bool = False


class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: Email
    password_hash: Optional[str] = None
    full_name: str
    phone: Optional[Phone] = None
    role: UserRole = UserRole.USER
    language: Language = Language.EN
    verification_code: Optional[str] = None
    reset_token: Optional[str] = None
    reset_token_expiry: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    preferences: Optional[UserPreferences] = None

    favorites: List[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
