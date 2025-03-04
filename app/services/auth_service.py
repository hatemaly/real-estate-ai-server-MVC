# app/services/auth_service.py
# This module contains the AuthService class which implements authentication-related
# business logic. It handles OAuth token verification, JWT token generation,
# and user authentication from tokens.

from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import httpx
from app.models.user_models.user import User, Email
from app.services.user_service import UserService
from app.config import settings


class AuthService:
    """
    Service class for handling authentication-related business logic.
    
    This service provides methods for verifying third-party OAuth tokens,
    creating JWT access tokens, and retrieving users from tokens.
    It works with the UserService to handle user operations.
    
    Attributes:
        user_service: The service that handles user operations
    """
    def __init__(self, user_service: UserService):
        """
        Initialize the authentication service with a user service.
        
        Args:
            user_service: The service that will handle user operations
        """
        self.user_service = user_service

    async def verify_google_token(self, token: str) -> dict:
        """
        Verify a Google OAuth token and retrieve user information.
        
        This method makes an HTTP request to Google's authentication API
        to verify the token and retrieve the associated user profile.
        
        Args:
            token: The Google OAuth token to verify
            
        Returns:
            dict: User information from Google (email, name, etc.)
            
        Raises:
            ValueError: If the token is invalid or verification fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise ValueError("Failed to verify Google token")
            return response.json()

    async def create_access_token(self, data: dict) -> str:
        """
        Create a JWT access token for authenticated users.
        
        This method generates a signed JWT token with the provided data
        and an expiration time based on the application settings.
        
        Args:
            data: Dictionary of data to encode in the token (must include 'sub')
            
        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        Get a user from a JWT token.
        
        This method decodes and validates the JWT token, then retrieves
        the corresponding user based on the email in the token's payload.
        
        Args:
            token: The JWT token to decode and validate
            
        Returns:
            Optional[User]: The user associated with the token, or None if invalid
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            email = payload.get("sub")
            if email is None:
                return None
            users = await self.user_service.get_users_by_email(email)
            if users and len(users) > 0:
                return users[0]
        except JWTError:
            return None
        return None