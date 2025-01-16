# app/routers/property_router.py
from fastapi import APIRouter, Depends
from typing import List
from app.controllers.property_controller import PropertyController
from app.repositories.property_repository import PropertyRepository
from app.database.collections import get_property_collection
from app.services.property_service import PropertyService
from app.models.property_models.property import Property

router = APIRouter()

async def get_property_controller() -> PropertyController:
    property_collection = await get_property_collection()
    repository = PropertyRepository(property_collection)
    service = PropertyService(repository)
    return PropertyController(service)

@router.post("/", response_model=Property)
async def create_property(property: Property, controller: PropertyController = Depends(get_property_controller)):
    return await controller.create_property(property)

@router.get("/{property_id}", response_model=Property)
async def get_property(property_id: str, controller: PropertyController = Depends(get_property_controller)):
    return await controller.get_property_by_id(property_id)

@router.get("/", response_model=List[str])
async def get_all_properties(controller: PropertyController = Depends(get_property_controller)):
    return await controller.get_all_properties()

@router.put("/", response_model=Property)
async def update_property(property: Property, controller: PropertyController = Depends(get_property_controller)):
    return await controller.update_property(property)

@router.delete("/{property_id}")
async def delete_property(property_id: str, controller: PropertyController = Depends(get_property_controller)):
    await controller.delete_property(property_id)
    return {"message": "Property deleted successfully"}
