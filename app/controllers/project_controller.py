# app/controllers/project_controller.py
from typing import List
from app.services.project_service import ProjectService
from app.models.developer_models.project import Project


class ProjectController:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    async def create_project(self, project: Project) -> Project:
        return await self.project_service.create_project(project)

    async def get_project_by_id(self, project_id: str) -> Project:
        return await self.project_service.get_project_by_id(project_id)

    async def get_all_projects(self) -> List[Project]:
        return await self.project_service.get_all_projects()

    async def update_project(self, project: Project) -> Project:
        return await self.project_service.update_project(project)

    async def delete_project(self, project_id: str) -> None:
        await self.project_service.delete_project(project_id)
