# app/repositories/base_repository.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Type

from pydantic import BaseModel
from sqlalchemy.cyextension.collections import Collection
from sqlalchemy.orm import Session

T = TypeVar("T")
ID = TypeVar("ID")

class BaseRepository(ABC, Generic[T, ID]):
    def __init__(self, collection: Collection, model: Type[BaseModel]):
        self.collection = collection
        self.model = model

    async def save(self, aggregate: BaseModel) -> None:
        document = aggregate.dict(by_alias=True)
        await self.collection.insert_one(document)

    async def delete(self, aggregate_id: str) -> None:
        await self.collection.delete_one({"_id": aggregate_id})

    async def update(self, aggregate: BaseModel) -> None:
        document = aggregate.dict(by_alias=True)
        await self.collection.replace_one({"_id": aggregate.id}, document)

    async def get_by_id(self, aggregate_id: str) -> Optional[BaseModel]:
        print(aggregate_id , " from fast api\n\n\n")
        print(self.collection , " \n " , self.model)
        document = await self.collection.find_one({"_id": aggregate_id})
        print("Document from DB:", document)
        if document:
            return self.model(**document)
        return None


    async def activate(self, aggregate_id: str) -> None:
        await self.collection.update_one({"_id": aggregate_id}, {"$set": {"is_active": True}})

    async def deactivate(self, aggregate_id: str) -> None:
        await self.collection.update_one({"_id": aggregate_id}, {"$set": {"is_active": False}})