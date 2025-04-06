# app/routers/project_router.py
from fastapi import APIRouter, Depends
from typing import List
from app.controllers.project_controller import ProjectController
from app.repositories.project_repository import ProjectRepository
from app.database.collections import get_project_collection
from app.services.project_service import ProjectService
from app.models.project_models.project import Project

router = APIRouter()

async def get_project_controller() -> ProjectController:
    project_collection = await get_project_collection()
    repository = ProjectRepository(project_collection)
    service = ProjectService(repository)
    return ProjectController(service)

@router.post("/", response_model=Project)
async def create_project(project: Project, controller: ProjectController = Depends(get_project_controller)):
    return await controller.create_project(project)

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str, controller: ProjectController = Depends(get_project_controller)):
    return await controller.get_project_by_id(project_id)

@router.get("/", response_model=List[Project])
async def get_all_projects(controller: ProjectController = Depends(get_project_controller)):
    return await controller.get_all_projects()

@router.put("/", response_model=Project)
async def update_project(project: Project, controller: ProjectController = Depends(get_project_controller)):
    return await controller.update_project(project)

@router.delete("/{project_id}")
async def delete_project(project_id: str, controller: ProjectController = Depends(get_project_controller)):
    await controller.delete_project(project_id)
    return {"message": "Project deleted successfully"}
