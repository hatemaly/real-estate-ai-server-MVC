from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.database.collections import get_user_collection
from app.models.auth_models import (
    Token, UserRegisterRequest, UserLoginRequest,
    SocialLoginRequest, VerifyEmailRequest,
    ResendVerificationRequest, ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.config import settings
import httpx
from app.controllers.auth_controller import AuthController

# Dependency to get AuthController
async def get_auth_controller() -> AuthController:
    user_collection = await get_user_collection()
    user_repo = UserRepository(user_collection)
    user_service = UserService(user_repo)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Google OAuth Token Endpoint
@router.post("/google-token")
async def get_google_token(
    code: str,
    redirect_uri: str = "http://localhost:8000/auth/google/callback",
):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Google API error: {e.response.text}"
            )

# Google OAuth login
@router.post('/social-login', response_model=Token)
async def social_login(request: SocialLoginRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.social_login(request)

# Register a new user
@router.post("/register", response_model=Token)
async def register(request: UserRegisterRequest, controller: AuthController = Depends(get_auth_controller)):
    return  {"message": "User registered successfully"}
    return await controller.register(request)

# Login with email and password
@router.post("/login", response_model=Token)
async def login(request: UserLoginRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.login(request)

# Email verification
@router.post("/verify-email")
async def verify_email(request: VerifyEmailRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.verify_email(request)

# Resend verification email
@router.post("/resend-verification")
async def resend_verification(request: ResendVerificationRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.resend_verification(request)

# Forgot password
@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.forgot_password(request)

# Reset password
@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.reset_password(request)
