from pymongo.collection import Collection
from typing import List, Optional
from app.models.developer_models.project import Project
from app.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, Project)

    async def get_by_name(self, name: str) -> Optional[Project]:
        document = await self.collection.find_one({"basic_info.name": name})
        if document:
            return self.model(**document)
        return None

    async def get_all(self) -> List[Project]:
        cursor = self.collection.find({})
        documents = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in documents]
