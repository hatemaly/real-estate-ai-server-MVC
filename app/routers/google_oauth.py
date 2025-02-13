from fastapi import APIRouter, HTTPException
from authlib.integrations.starlette_client import OAuth
from app.config import settings
from fastapi import Depends, Request
from app.models.auth_models import Token, SocialLoginRequest
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.database.collections import get_user_collection

# Initialize OAuth client
oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri="http://localhost:4200/login",
    client_kwargs={"scope": "openid profile email"},
)

# Dependency to get AuthController
async def get_auth_controller() -> AuthController:
    user_collection = await get_user_collection()
    user_repo = UserRepository(user_collection)
    user_service = UserService(user_repo)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)

router = APIRouter(prefix="/auth/google", tags=["Google OAuth"])

# Google OAuth callback
@router.get("/callback")
async def google_callback(request: Request, controller: AuthController = Depends(get_auth_controller)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)

    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    # Handle user registration or login with Google data
    return await controller.social_login(SocialLoginRequest(provider="google", token=token['access_token']))
