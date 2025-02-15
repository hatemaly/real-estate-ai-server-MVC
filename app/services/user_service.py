from typing import List, Optional
from app.models.user_models.user import User, Language
from app.repositories.user_repository import UserRepository

class \
        UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return await self.repository.get_by_email(email)

    async def update_user(self, user: User) -> User:
        """Update user details"""
        await self.repository.update(user)
        return user

    async def create_user(self, user: User) -> User:
        """Create new user"""
        created_user = await self.repository.create_user(user)
        return created_user

    async def update_user_details(self, user_id: str, full_name: Optional[str] = None, phone: Optional[str] = None, language: Optional[str] = None) -> User:
        """Update user details like full name, phone, and language"""
        user = await self.get_user_by_id(user_id)
        if full_name:
            user.full_name = full_name
        if phone:
            user.phone = phone  # Directly update phone as string
        if language:
            user.language = Language(language)

        await self.repository.update(user)
        return user

    async def add_favorite(self, user_id: str, property_id: str) -> None:
        """Add property to user favorites"""
        await self.repository.add_favorite(user_id, property_id)

    async def remove_favorite(self, user_id: str, property_id: str) -> None:
        """Remove property from user favorites"""
        await self.repository.remove_favorite(user_id, property_id)

    async def get_favorites(self, user_id: str, page: int = 1, limit: int = 10) -> dict:
        """Get user favorites with pagination"""
        user = await self.get_user_by_id(user_id)
        total = len(user.favorites)
        skip = (page - 1) * limit
        favorites_paginated = user.favorites[skip: skip + limit]
        return {
            "favorite_properties": [{"property_id": prop} for prop in favorites_paginated],
            "total": total
        }
