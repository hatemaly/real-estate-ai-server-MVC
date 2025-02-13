from app.models.base_model import BaseModelApp
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime

class SocialProvider(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    APPLE = "apple"
    MICROSOFT = "microsoft"

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    AGENT = "agent"

class Language(str, Enum):
    EN = "en"
    AR = "ar"

class User(BaseModelApp):
    email: EmailStr               # Primary verified email
    first_name: str
    last_name: str
    social_providers: List[SocialProvider] = Field(default_factory=list)  # Track OAuth providers used
    role: UserRole = UserRole.USER
    language: Language = Language.EN
    phone: Optional[str] = None
    favorites: List[str] = Field(default_factory=list)
    hashed_password: Optional[str] = None  # Present for email/password users
    is_verified: bool = False     # Email verification status

class SocialAccount(BaseModelApp):
    user_id: str                  # Reference to User document
    provider: SocialProvider
    provider_user_id: str         # Unique ID from provider
    access_token: str             # Current valid token
    refresh_token: Optional[str]  # For token renewal
    expires_at: datetime          # Token expiration
    scopes: List[str]             # Granted permissions (e.g., ["email", "profile"])

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

class EmailVerificationToken(BaseModelApp):
    user_id: str = Field(...)     # Reference to User document
    token: str = Field(...)       # Unique verification token
    expires_at: datetime = Field(...)  # Token expiration time
    used: bool = Field(default=False)  # Prevent token reuse

    def is_valid(self):
        return not self.used and datetime.utcnow() < self.expires_at

