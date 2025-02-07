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

    async def get_me(self, user_id: str) -> User:
        return await self.user_service.get_current_user(user_id)

    async def update_me(self, user_id: str, full_name: str = None, phone: str = None, language: str = None) -> User:
        return await self.user_service.update_current_user(user_id, full_name, phone, language)

    async def get_my_favorites(self, user_id: str, page: int, limit: int) -> dict:
        return await self.user_service.get_favorites(user_id, page, limit)

    async def add_to_my_favorites(self, user_id: str, property_id: str) -> None:
        await self.user_service.add_favorite(user_id, property_id)

    async def remove_from_my_favorites(self, user_id: str, property_id: str) -> None:
        await self.user_service.remove_favorite(user_id, property_id)
