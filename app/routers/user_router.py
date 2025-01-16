# app/routers/user_router.py
from fastapi import APIRouter, Depends
from typing import List
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

@router.post("/", response_model=User)
async def create_user(user: User, controller: UserController = Depends(get_user_controller)):
    return await controller.create_user(user)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, controller: UserController = Depends(get_user_controller)):
    print(user_id , "\n\n")
    return await controller.get_user_by_id(user_id)

@router.get("/", response_model=List[User])
async def get_users_by_role(
    role: str, skip: int = 0, limit: int = 10, controller: UserController = Depends(get_user_controller)
):
    return await controller.get_users_by_role(role, skip, limit)

@router.put("/", response_model=User)
async def update_user(user: User, controller: UserController = Depends(get_user_controller)):
    return await controller.update_user(user)

@router.delete("/{user_id}")
async def delete_user(user_id: str, controller: UserController = Depends(get_user_controller)):
    await controller.delete_user(user_id)
    return {"message": "User deleted successfully"}
