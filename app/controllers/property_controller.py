# app/controllers/property_controller.py
from typing import List
from app.services.property_service import PropertyService
from app.models.property_models.property import Property


class PropertyController:
    def __init__(self, property_service: PropertyService):
        self.property_service = property_service

    async def create_property(self, property: Property) -> Property:
        return await self.property_service.create_property(property)

    async def get_property_by_id(self, property_id: str) -> Property:
        return await self.property_service.get_property_by_id(property_id)

    async def get_all_properties(self) -> List[str]:
        return await self.property_service.get_all_property_ids()

    async def update_property(self, property: Property) -> Property:
        return await self.property_service.update_property(property)

    async def delete_property(self, property_id: str) -> None:
        await self.property_service.delete_property(property_id)
