from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Optional

from app.controllers.user_controller import UserController
from app.repositories.user_repository import UserRepository
from app.database.collections import get_user_collection
from app.services.user_service import UserService
from app.models.user_models.user import User

router = APIRouter()


async def get_user_controller() -> UserController:
    user_collection = await get_user_collection()
    repository = UserRepository(user_collection)
    service = UserService(repository)
    return UserController(service)


async def get_current_user_id(request: Request) -> str:
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user_id


@router.post("/", response_model=User)
async def create_user(
    user: User,
    controller: UserController = Depends(get_user_controller)
):
    return await controller.create_user(user)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    controller: UserController = Depends(get_user_controller)
):
    return await controller.get_user_by_id(user_id)


@router.get("/", response_model=List[User])
async def get_users_by_role(
    role: str,
    skip: int = 0,
    limit: int = 10,
    controller: UserController = Depends(get_user_controller)
):
    return await controller.get_users_by_role(role, skip, limit)


@router.put("/", response_model=User)
async def update_user(
    user: User,
    controller: UserController = Depends(get_user_controller)
):
    return await controller.update_user(user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    controller: UserController = Depends(get_user_controller)
):
    await controller.delete_user(user_id)
    return {"message": "User deleted successfully"}


# 1) GET /api/v1/users/me
@router.get("/me", response_model=User)
async def get_me(
    controller: UserController = Depends(get_user_controller),
    current_user_id: str = Depends(get_current_user_id),
):
    return await controller.get_me(current_user_id)


# 2) PUT /api/v1/users/me
@router.put("/me", response_model=User)
async def update_me(
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
    language: Optional[str] = None,
    controller: UserController = Depends(get_user_controller),
    current_user_id: str = Depends(get_current_user_id),
):
    return await controller.update_me(current_user_id, full_name, phone, language)


# 3) GET /api/v1/users/me/favorites
@router.get("/me/favorites")
async def get_my_favorites(
    page: int = 1,
    limit: int = 10,
    controller: UserController = Depends(get_user_controller),
    current_user_id: str = Depends(get_current_user_id),
):
    return await controller.get_my_favorites(current_user_id, page, limit)


# 4) POST /api/v1/users/me/favorites/{property_id}
@router.post("/me/favorites/{property_id}")
async def add_property_to_favorites(
    property_id: str,
    controller: UserController = Depends(get_user_controller),
    current_user_id: str = Depends(get_current_user_id),
):
    await controller.add_to_my_favorites(current_user_id, property_id)
    return {"success": True}


# 5) DELETE /api/v1/users/me/favorites/{property_id}
@router.delete("/me/favorites/{property_id}")
async def remove_property_from_favorites(
    property_id: str,
    controller: UserController = Depends(get_user_controller),
    current_user_id: str = Depends(get_current_user_id),
):
    await controller.remove_from_my_favorites(current_user_id, property_id)
    return {"success": True}
