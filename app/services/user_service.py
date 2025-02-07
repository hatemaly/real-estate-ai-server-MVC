from typing import List, Optional
from app.models.user_models.user import User, Phone, Language
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user: User) -> User:
        await self.repository.save(user)
        return user

    async def update_user(self, user: User) -> User:
        await self.repository.update(user)
        return user

    async def delete_user(self, user_id: str) -> None:
        await self.repository.delete(user_id)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return await self.repository.get_by_id(user_id)

    async def get_users_by_email(self, email: str) -> Optional[User]:
        return await self.repository.get_by_email(email)

    async def get_users_by_role(self, role: str, skip: int = 0, limit: int = 50) -> List[User]:
        return await self.repository.get_users_by_role(role, skip, limit)

    async def get_users_ids_by_role(self, role: str) -> List[str]:
        return await self.repository.get_users_ids_by_role(role)

    async def activate_user(self, user_id: str) -> None:
        await self.repository.activate(user_id)

    async def deactivate_user(self, user_id: str) -> None:
        await self.repository.deactivate(user_id)


    async def get_current_user(self, user_id: str) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    async def update_current_user(
            self,
            user_id: str,
            full_name: Optional[str] = None,
            phone: Optional[str] = None,
            language: Optional[str] = None
    ) -> User:
        user = await self.get_current_user(user_id)
        if full_name is not None:
            user.full_name = full_name

        if phone is not None:
            if user.phone is None:
                user.phone = Phone(number=phone, is_verified=False)
            else:
                user.phone.number = phone

        if language is not None:
            if language in [lang.value for lang in Language]:
                user.language = Language(language)

        await self.repository.update(user)
        return user


    async def get_favorites(self, user_id: str, page: int = 1, limit: int = 10) -> dict:
        user = await self.get_current_user(user_id)

        total = len(user.favorites)
        skip = (page - 1) * limit
        favorites_paginated = user.favorites[skip: skip + limit]

        return {
            "favorite_properties": [{"property_id": prop} for prop in favorites_paginated],
            "total": total
        }

    async def add_favorite(self, user_id: str, property_id: str) -> None:
        # يمكن التحقق أولًا من صلاحية property_id أو وجوده
        # مثال: await self.property_repository.get_by_id(property_id)
        await self.repository.add_favorite(user_id, property_id)

    async def remove_favorite(self, user_id: str, property_id: str) -> None:
        await self.repository.remove_favorite(user_id, property_id)
