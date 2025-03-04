# app/routers/auth_router.py
# This module defines the FastAPI router for authentication-related endpoints.
# It provides routes for user authentication, retrieving the current user,
# and testing protected routes that require authentication.

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.database.collections import get_user_collection
from app.models.auth_models import Token
from app.models.user_models.user import User

# Create an API router for authentication endpoints
router = APIRouter()

# Configure OAuth2 password bearer for token extraction from requests
# The tokenUrl parameter specifies the endpoint that returns access tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_auth_controller() -> AuthController:
    """
    Dependency injection function to create and provide an AuthController instance.
    
    This function follows the repository pattern, creating the entire dependency chain:
    database collection -> repository -> user service -> auth service -> controller
    
    Returns:
        AuthController: A configured controller for handling authentication operations
    """
    user_collection = await get_user_collection()
    repository = UserRepository(user_collection)
    user_service = UserService(repository)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)

@router.post("/login/google", response_model=Token)
async def google_login(token: str, controller: AuthController = Depends(get_auth_controller)):
    """
    Authenticate a user using Google OAuth token.
    
    This endpoint verifies the Google token, creates a user if they don't exist yet,
    and returns an access token for the application.
    
    Args:
        token: Google OAuth token obtained from the client
        controller: AuthController instance (injected dependency)
    
    Returns:
        Token: An application access token for the authenticated session
        
    Raises:
        HTTPException: If Google authentication fails
    """
    return await controller.google_login(token)

@router.get("/me", response_model=User)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    controller: AuthController = Depends(get_auth_controller)
):
    """
    Get the current authenticated user's profile.
    
    This endpoint extracts the JWT token from the request, validates it,
    and returns the corresponding user's profile.
    
    Args:
        token: JWT token extracted from the request header (via oauth2_scheme)
        controller: AuthController instance (injected dependency)
    
    Returns:
        User: The authenticated user's profile
        
    Raises:
        HTTPException: If authentication fails or the token is invalid
    """
    user = await controller.auth_service.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_user)
):
    """
    Example of a protected route that requires authentication.
    
    This endpoint can only be accessed by authenticated users. It uses the
    get_current_user dependency to ensure the request includes valid credentials.
    
    Args:
        current_user: The authenticated user (from get_current_user dependency)
    
    Returns:
        dict: A message and the user object
    """
    return {"message": "This is protected", "user": current_user}