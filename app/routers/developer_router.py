# app/routers/developer_router.py
from fastapi import APIRouter, Depends
from typing import List
from app.controllers.developer_controller import DeveloperController
from app.repositories.developer_repository import DeveloperRepository
from app.database.collections import get_developer_collection
from app.services.developer_service import DeveloperService
from app.models.developer_models.developer import Developer

router = APIRouter()

async def get_developer_controller() -> DeveloperController:
    developer_collection = await get_developer_collection()
    repository = DeveloperRepository(developer_collection)
    service = DeveloperService(repository)
    return DeveloperController(service)

@router.post("/", response_model=Developer)
async def create_developer(developer: Developer, controller: DeveloperController = Depends(get_developer_controller)):
    return await controller.create_developer(developer)

@router.get("/{developer_id}", response_model=Developer)
async def get_developer(developer_id: str, controller: DeveloperController = Depends(get_developer_controller)):
    return await controller.get_developer_by_id(developer_id)

@router.get("/", response_model=List[Developer])
async def get_all_developers(controller: DeveloperController = Depends(get_developer_controller)):
    return await controller.get_all_developers()

@router.put("/", response_model=Developer)
async def update_developer(developer: Developer, controller: DeveloperController = Depends(get_developer_controller)):
    return await controller.update_developer(developer)

@router.delete("/{developer_id}")
async def delete_developer(developer_id: str, controller: DeveloperController = Depends(get_developer_controller)):
    await controller.delete_developer(developer_id)
    return {"message": "Developer deleted successfully"}
