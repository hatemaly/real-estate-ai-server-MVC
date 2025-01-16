from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum
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
    id: Optional[str] = Field(alias="_id")  # MongoDB's primary key
    email: Email
    full_name: str
    role: UserRole
    language: Language
    phone: Optional[Phone] = None
    preferences: Optional[UserPreferences] = None  # Explicitly linked preferences

    class Config:
        arbitrary_types_allowed = True


UserPreferences.model_rebuild()
User.model_rebuild()
