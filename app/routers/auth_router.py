from http.client import HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from fastapi import APIRouter, Request, Query
from .google_oauth import oauth
from fastapi import APIRouter, Depends
from app.controllers.auth_controller import AuthController
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
from fastapi import APIRouter, Query, HTTPException
import httpx
from app.config import settings


async def get_auth_controller() -> AuthController:
    user_collection = await get_user_collection()
    user_repo = UserRepository(user_collection)
    user_service = UserService(user_repo)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)


class GoogleLoginRequest(BaseModel):
    redirect_uri: str = "http://localhost:8000/auth/google/callback"

router = APIRouter(prefix="/auth", tags=["Authentication"])

# @router.post("/google-token")
# async def get_google_token(
#     code: str = Query(..., description="Authorization code from Google"),
#     redirect_uri: str = Query("http://localhost:8000/auth/google/callback")
# ):
#     token_url = "https://oauth2.googleapis.com/token"
#     data = {
#         "code": code,
#         "client_id": settings.GOOGLE_CLIENT_ID,
#         "client_secret": settings.GOOGLE_CLIENT_SECRET,
#         "redirect_uri": redirect_uri,
#         "grant_type": "authorization_code",
#     }
#
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.post(token_url, data=data)
#             response.raise_for_status()
#             return response.json()
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(
#                 status_code=e.response.status_code,
#                 detail=f"Google API error: {e.response.text}"
#             )

@router.post('/auth/login/google')
async def login_google(
        code: str = Query(..., description="Authorization code from Google"),
        redirect_uri: str = Query("http://localhost:8000/auth/google/callback")
):
    """
    Handle Google OAuth login with authorization code
    """
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
            token_response = await client.post(token_url, data=data)
            token_response.raise_for_status()
            tokens = token_response.json()

            # Get user info
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {tokens['access_token']}"}
            )
            user_info = user_response.json()

            # Your user creation/login logic here
            # ...

            return {
                "access_token": tokens['access_token'],
                "user_info": user_info
            }

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Google API error: {e.response.text}"
            )
@router.get('/auth/google/callback')
async def auth_google_callback(request: Request):
    """
    Callback endpoint for Google OAuth
    Returns access token and user info
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not token:
        raise HTTPException(status_code=400, detail="Failed to fetch access token")

    user_info = await oauth.google.parse_id_token(request, token)
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    # Create your own JWT token or use Google's token
    return {
        "access_token": token['access_token'],
        "token_type": "bearer",
        "user_info": {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture")
        }
    }
@router.post("/register", response_model=Token)
async def register(request: UserRegisterRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.register(request)

# @router.post("/login", response_model=Token)
# async def login(request: UserLoginRequest, controller: AuthController = Depends(get_auth_controller)):
#     return await controller.login(request)

@router.post("/social-login", response_model=Token)
async def social_login(request: SocialLoginRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.social_login(request)

@router.post("/verify-email")
async def verify_email(request: VerifyEmailRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.verify_email(request)

@router.post("/resend-verification")
async def resend_verification(request: ResendVerificationRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.resend_verification(request)

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.forgot_password(request)

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, controller: AuthController = Depends(get_auth_controller)):
    return await controller.reset_password(request)