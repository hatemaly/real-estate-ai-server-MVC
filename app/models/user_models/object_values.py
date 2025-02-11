# src/models/user_models/object_values.py
from enum import Enum
from pydantic import BaseModel, EmailStr



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
