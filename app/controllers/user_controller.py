# src/controllers/user_controller.py
from typing import List
from app.services.user_service import UserService
from app.models.user_models.user import User


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def create_user(self, user: User) -> User:
        return await self.user_service.create_user(user)

    async def get_user_by_id(self, user_id: str) -> User:
        return await self.user_service.get_user_by_id(user_id)

    async def get_users_by_role(self, role: str, skip: int, limit: int) -> List[User]:
        return await self.user_service.get_users_by_role(role, skip, limit)

    async def update_user(self, user: User) -> User:
        return await self.user_service.update_user(user)

    async def delete_user(self, user_id: str) -> None:
        await self.user_service.delete_user(user_id)
