# app/repositories/appointment_repository.py
from typing import Optional, List
from datetime import datetime

from pymongo.collection import Collection
from bson import ObjectId
from app.models.user_models.appointment_request import AppointmentRequest, AppointmentType, RequestStatus
from app.repositories.base_repository import BaseRepository

class AppointmentRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, AppointmentRequest)

    async def find_appointments(
        self,
        customer_id: str,
        appointment_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[AppointmentRequest]:
        query = {"customer_id": customer_id}

        if appointment_type:
            query["appointment_type"] = appointment_type
        if status:
            query["status"] = status

        cursor = self.collection.find(query).skip(skip).limit(limit)
        results = []
        async for doc in cursor:
            results.append(AppointmentRequest(**doc))
        return results

    async def count_appointments(
        self,
        customer_id: str,
        appointment_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> int:
        query = {"customer_id": customer_id}

        if appointment_type:
            query["appointment_type"] = appointment_type
        if status:
            query["status"] = status

        return await self.collection.count_documents(query)

    async def get_by_id_and_customer(self, appointment_id: str, customer_id: str) -> Optional[AppointmentRequest]:
        doc = await self.collection.find_one({"_id": appointment_id, "customer_id": customer_id})
        if doc:
            return AppointmentRequest(**doc)
        return None

