# src/services/user_service.py
from typing import List, Optional
from app.models.user_models.user import User
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
        print(user_id , " from service \n\n")
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
