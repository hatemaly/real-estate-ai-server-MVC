# src/models/user_models/user.py
# This module defines the core user models for the real estate application.
# It includes user roles, contact information, language preferences, and user metadata.

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum
from app.models.user_models.user_preferences import UserPreferences


class UserRole(str, Enum):
    """
    Enumeration of user roles within the system.
    
    These roles determine the permissions and access levels for each user.
    
    Values:
        USER: Standard user/customer role with basic permissions
        ADMIN: Administrative role with full system access
        AGENT: Real estate agent/broker role with property management permissions
    """
    USER = "user"  # Standard user/customer
    ADMIN = "admin"  # Administrator with full access
    AGENT = "agent"  # Real estate agent/broker


class Language(str, Enum):
    """
    Enumeration of supported languages for the user interface.
    
    The selected language affects the user interface and communications.
    
    Values:
        EN: English language
        AR: Arabic language
    """
    EN = "en"  # English
    AR = "ar"  # Arabic


class Email(BaseModel):
    """
    Model for storing and tracking user email addresses.
    
    Includes verification status to ensure email validity.
    
    Attributes:
        address: The user's email address (validated format)
        is_verified: Whether the email has been verified
    """
    address: EmailStr  # Email address (validated format)
    is_verified: bool = False  # Whether email is verified


class Phone(BaseModel):
    """
    Model for storing and tracking user phone numbers.
    
    Includes verification status to ensure phone validity.
    
    Attributes:
        number: The user's phone number
        is_verified: Whether the phone number has been verified
    """
    number: str  # Phone number
    is_verified: bool = False  # Whether phone is verified


class User(BaseModel):
    """
    Core user model representing a user in the system.
    
    This model contains all essential user information including identity,
    contact details, preferences, and system role.
    
    Attributes:
        id: Unique identifier for the user (MongoDB ObjectId)
        email: User's email address information
        full_name: User's full name
        role: User's role in the system (user, admin, or agent)
        language: User's preferred language for the interface
        phone: User's phone number information (optional)
        preferences: User's property search preferences (optional)
    """
    id: Optional[str] = Field(alias="_id")  # MongoDB's primary key
    email: Email  # User's email information
    full_name: str  # User's full name
    role: UserRole  # User's role in the system
    language: Language  # User's preferred language
    phone: Optional[Phone] = None  # User's phone information (optional)
    preferences: Optional[UserPreferences] = None  # Explicitly linked preferences

    class Config:
        """Configuration for the User model."""
        arbitrary_types_allowed = True  # Allow arbitrary types


UserPreferences.model_rebuild()
User.model_rebuild()
