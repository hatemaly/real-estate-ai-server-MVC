# src/services/developer_service.py
from typing import List, Optional
from app.models.developer_models.developer import Developer
from app.repositories.developer_repository import DeveloperRepository


class DeveloperService:
    def __init__(self, repository: DeveloperRepository):
        self.repository = repository

    async def create_developer(self, developer: Developer) -> Developer:
        await self.repository.save(developer)
        return developer

    async def update_developer(self, developer: Developer) -> Developer:
        await self.repository.update(developer)
        return developer

    async def delete_developer(self, developer_id: str) -> None:
        await self.repository.delete(developer_id)

    async def get_developer_by_id(self, developer_id: str) -> Optional[Developer]:
        return await self.repository.get_by_id(developer_id)

    async def get_all_developers(self) -> List[Developer]:
        return await self.repository.get_all()
