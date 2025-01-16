# src/services/project_service.py
from typing import List, Optional
from app.models.developer_models.project import Project
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(self, project: Project) -> Project:
        await self.repository.save(project)
        return project

    async def update_project(self, project: Project) -> Project:
        await self.repository.update(project)
        return project

    async def delete_project(self, project_id: str) -> None:
        await self.repository.delete(project_id)

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        return await self.repository.get_by_id(project_id)

    async def get_project_by_name(self, name: str) -> Optional[Project]:
        return await self.repository.get_by_name(name)

    async def get_all_projects(self) -> List[Project]:
        return await self.repository.get_all()
