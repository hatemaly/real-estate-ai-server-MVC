# src/models/user_models/auth_credential.py

from typing import Optional
from datetime import datetime
from enum import Enum

from app.models.base_model import BaseModelApp


class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    MICROSOFT = "microsoft"


class AuthInfo(BaseModelApp):
    provider: AuthProvider
    provider_user_id: Optional[str] = None
    phone: Optional[str] = None
    password_hash: Optional[str] = None
    verified_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    is_primary: bool = False


class AuthCredential(BaseModelApp):
    auth_info: AuthInfo
    revoked: bool = False
    revoked_at: Optional[datetime] = None

    def revoke(self):
        self.revoked = True
        self.revoked_at = datetime.now()
