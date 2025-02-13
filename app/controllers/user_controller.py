from typing import List
from fastapi import HTTPException, Depends
from app.services.user_service import UserService
from app.models.user_models.user import User
# from app.models.user_models.preferences import UserPreferences

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    # Get current user info
    async def get_me(self, user_id: str) -> User:
        user = await self.user_service.get_current_user(user_id)
        return user

    # Update current user info
    async def update_me(self, user_id: str, full_name: str = None, phone: str = None, language: str = None) -> User:
        return await self.user_service.update_current_user(user_id, full_name, phone, language)

    # Get user favorites with pagination
    async def get_my_favorites(self, user_id: str, page: int = 1, limit: int = 10) -> dict:
        return await self.user_service.get_favorites(user_id, page, limit)

    # Add property to user favorites
    async def add_to_my_favorites(self, user_id: str, property_id: str) -> dict:
        await self.user_service.add_favorite(user_id, property_id)
        return {"success": True}

    # Remove property from user favorites
    async def remove_from_my_favorites(self, user_id: str, property_id: str) -> dict:
        await self.user_service.remove_favorite(user_id, property_id)
        return {"success": True}
