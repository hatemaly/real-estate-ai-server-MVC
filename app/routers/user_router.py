from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Optional
from app.controllers.user_controller import UserController
from app.database.collections import get_user_collection
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.models.user_models.user import User

router = APIRouter()

# Dependency to get UserController
async def get_user_controller() -> UserController:
    user_collection = await get_user_collection()
    repository = UserRepository(user_collection)
    service = UserService(repository)
    return UserController(service)

# Dependency to get current user's ID from request header
async def get_current_user_id(request: Request) -> str:
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user_id

# Get current user's details
@router.get("/me", response_model=User)
async def get_me(controller: UserController = Depends(get_user_controller), current_user_id: str = Depends(get_current_user_id)):
    return await controller.get_me(current_user_id)

# Update current user's details
@router.put("/me", response_model=User)
async def update_me(
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
    language: Optional[str] = None,
    controller: UserController = Depends(get_user_controller),
    current_user_id: str = Depends(get_current_user_id),
):
    return await controller.update_me(current_user_id, full_name, phone, language)

# Get user's favorite properties
@router.get("/me/favorites")
async def get_my_favorites(
    page: int = 1,
    limit: int = 10,
    controller: UserController = Depends(get_user_controller),
    current_user_id: str = Depends(get_current_user_id),
):
    return await controller.get_my_favorites(current_user_id, page, limit)

# Add property to favorites
@router.post("/me/favorites/{property_id}")
async def add_property_to_favorites(
    property_id: str,
    controller: UserController = Depends(get_user_controller),
    current_user_id: str = Depends(get_current_user_id),
):
    await controller.add_to_my_favorites(current_user_id, property_id)
    return {"success": True}

# Remove property from favorites
@router.delete("/me/favorites/{property_id}")
async def remove_property_from_favorites(
    property_id: str,
    controller: UserController = Depends(get_user_controller),
    current_user_id: str = Depends(get_current_user_id),
):
    await controller.remove_from_my_favorites(current_user_id, property_id)
    return {"success": True}
