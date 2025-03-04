# app/controllers/auth_controller.py
# This module contains the AuthController which handles authentication-related operations.
# It processes authentication requests, coordinates with the auth service layer,
# and manages user creation for new users during authentication.

from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.models.auth_models import Token
from app.models.user_models.user import User, Email, UserRole, Language


class AuthController:
    """
    Controller handling authentication operations in the application.
    
    This controller acts as an intermediary between the API routes and the auth service,
    processing authentication requests and handling error conditions.
    
    Attributes:
        auth_service: Service that implements authentication business logic
    """
    def __init__(self, auth_service: AuthService):
        """
        Initialize the authentication controller.
        
        Args:
            auth_service: The service that implements authentication logic
        """
        self.auth_service = auth_service

    async def google_login(self, token: str) -> Token:
        """
        Authenticate a user using Google OAuth.
        
        This method verifies the Google token, checks if the user exists in the system,
        creates a new user account if needed, and generates an access token for the session.
        
        Args:
            token: Google OAuth token obtained from the client
            
        Returns:
            Token: An application access token for the authenticated session
            
        Raises:
            HTTPException: If authentication fails for any reason
        """
        try:
            # Verify the Google token and get user information
            user_data = await self.auth_service.verify_google_token(token)

            # Check if user exists or create new user
            email = user_data.get("email")
            existing_users = await self.auth_service.user_service.get_users_by_email(email)

            if not existing_users:
                # Create new user if this is their first login
                new_user = User(
                    email=Email(address=email, is_verified=True),  # Email is verified via Google
                    full_name=user_data.get("name", ""),  # Get name from Google profile
                    role=UserRole.USER,  # Assign standard user role
                    language=Language.EN  # Default to English language
                )
                await self.auth_service.user_service.create_user(new_user)

            # Create an application access token
            access_token = await self.auth_service.create_access_token(
                {"sub": email}  # Use email as subject identifier
            )
            return Token(access_token=access_token)

        except Exception as e:
            # Convert any errors to HTTP exceptions
            raise HTTPException(status_code=400, detail=str(e))
