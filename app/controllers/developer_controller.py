# app/controllers/developer_controller.py
from typing import List
from app.services.developer_service import DeveloperService
from app.models.developer_models.developer import Developer


class DeveloperController:
    def __init__(self, developer_service: DeveloperService):
        self.developer_service = developer_service

    async def create_developer(self, developer: Developer) -> Developer:
        return await self.developer_service.create_developer(developer)

    async def get_developer_by_id(self, developer_id: str) -> Developer:
        return await self.developer_service.get_developer_by_id(developer_id)

    async def get_all_developers(self) -> List[Developer]:
        return await self.developer_service.get_all_developers()

    async def update_developer(self, developer: Developer) -> Developer:
        return await self.developer_service.update_developer(developer)

    async def delete_developer(self, developer_id: str) -> None:
        await self.developer_service.delete_developer(developer_id)
