# src/services/property_service.py
from typing import List, Optional
from app.models.property_models.property import Property
from app.repositories.property_repository import PropertyRepository


class PropertyService:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    async def create_property(self, property: Property) -> Property:
        await self.repository.save(property)
        return property

    async def update_property(self, property: Property) -> Property:
        await self.repository.update(property)
        return property

    async def delete_property(self, property_id: str) -> None:
        await self.repository.delete(property_id)

    async def get_property_by_id(self, property_id: str) -> Optional[Property]:
        return await self.repository.get_by_id(property_id)

    async def get_all_property_ids(self) -> List[str]:
        return await self.repository.get_all_ids()

    async def get_active_properties(self) -> List[str]:
        return await self.repository.get_active_properties_ids()

    async def activate_property(self, property_id: str) -> None:
        await self.repository.activate(property_id)

    async def deactivate_property(self, property_id: str) -> None:
        await self.repository.deactivate(property_id)
