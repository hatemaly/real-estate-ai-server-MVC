# src/models/user_models/auth_credential.py
# This module defines models related to user authentication credentials.
# It includes authentication providers, authentication information, and credential management.

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AuthProvider(str, Enum):
    """
    Enumeration of supported authentication providers.
    
    This enum defines the different authentication methods available to users.
    
    Values:
        EMAIL: Traditional email/password authentication
        GOOGLE: Authentication via Google OAuth
        FACEBOOK: Authentication via Facebook OAuth
        MICROSOFT: Authentication via Microsoft OAuth
    """
    EMAIL = "email"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    MICROSOFT = "microsoft"


class AuthInfo(BaseModel):
    """
    Model for storing authentication information for a specific provider.
    
    Attributes:
        provider: The authentication provider (email, Google, etc.)
        provider_user_id: User ID provided by the authentication provider
        phone: Phone number associated with this authentication method
        password_hash: Hashed password (for email authentication)
        verified_at: When the authentication method was verified
        last_login_at: When the user last logged in using this method
        is_primary: Whether this is the user's primary authentication method
    """
    provider: AuthProvider  # Authentication provider type
    provider_user_id: Optional[str] = None  # User ID from the provider
    phone: Optional[str] = None  # Associated phone number
    password_hash: Optional[str] = None  # Hashed password (for email auth)
    verified_at: Optional[datetime] = None  # When auth method was verified
    last_login_at: Optional[datetime] = None  # Last login timestamp
    is_primary: bool = False  # Whether this is the primary auth method


class AuthCredential(BaseModel):
    """
    Model for managing user authentication credentials.
    
    This model represents a complete authentication credential, which may
    be revoked if necessary (e.g., for security reasons).
    
    Attributes:
        id: Unique identifier for the credential (MongoDB ObjectId)
        auth_info: Information about the authentication method
        revoked: Whether the credential has been revoked
        revoked_at: When the credential was revoked, if applicable
    """
    id: Optional[str] = Field(alias="_id")  # MongoDB's primary key
    auth_info: AuthInfo  # Authentication information
    revoked: bool = False  # Whether credential is revoked
    revoked_at: Optional[datetime] = None  # When credential was revoked

    def revoke(self):
        """
        Revoke this authentication credential.
        
        This method marks the credential as revoked and sets the revocation timestamp.
        Used when a credential needs to be invalidated for security or other reasons.
        """
        self.revoked = True
        self.revoked_at = datetime.now()
