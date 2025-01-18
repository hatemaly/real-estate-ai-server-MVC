from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.database.collections import get_user_collection
from app.models.auth_models import Token
from app.models.user_models.user import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_auth_controller() -> AuthController:
    user_collection = await get_user_collection()
    repository = UserRepository(user_collection)
    user_service = UserService(repository)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)

@router.post("/login/google", response_model=Token)
async def google_login(token: str, controller: AuthController = Depends(get_auth_controller)):
    return await controller.google_login(token)

@router.get("/me", response_model=User)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    controller: AuthController = Depends(get_auth_controller)
):
    user = await controller.auth_service.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_user)
):
    return {"message": "This is protected", "user": current_user}