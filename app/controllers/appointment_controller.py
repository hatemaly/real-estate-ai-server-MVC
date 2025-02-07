# app/controllers/appointment_controller.py
from typing import Optional, List
from datetime import datetime

from app.services.appointment_service import AppointmentService
from app.models.user_models.appointment_request import AppointmentRequest


class AppointmentController:
    def __init__(self, appointment_service: AppointmentService):
        self.appointment_service = appointment_service

    async def get_appointments(self, user_id: str, appointment_type: Optional[str], status: Optional[str], page: int,
                               limit: int):
        items, total = await self.appointment_service.get_appointments(user_id, appointment_type, status, page, limit)

        result_items = []
        for appt in items:
            item_dict = await self.appointment_service.build_appointment_response(appt)
            result_items.append(item_dict)

        return {
            "items": result_items,
            "total": total
        }

    async def create_appointment(self, user_id: str, property_ids: List[str], appointment_type: Optional[str]):
        appt = await self.appointment_service.create_appointment(user_id, property_ids, appointment_type)
        return {
            "id": appt.id,
            "status": appt.status,
            "request_timestamp": appt.request_timestamp,
            "properties": [{"id": pid} for pid in appt.property_id]
        }

    async def approve_appointment(self, user_id: str, appointment_id: str, broker_id: str, timestamp: datetime):
        await self.appointment_service.approve_appointment(user_id, appointment_id, broker_id, timestamp)

    async def reject_appointment(self, user_id: str, appointment_id: str, reason: str):
        await self.appointment_service.reject_appointment(user_id, appointment_id, reason)

    async def cancel_appointment(self, user_id: str, appointment_id: str, reason: str):
        await self.appointment_service.cancel_appointment(user_id, appointment_id, reason)

    async def fulfill_appointment(self, user_id: str, appointment_id: str, moms: str, broker_id: Optional[str],
                                  timestamp: Optional[datetime]):
        await self.appointment_service.fulfill_appointment(user_id, appointment_id, moms, broker_id, timestamp)

    async def reschedule_appointment(
            self,
            user_id: str,
            appointment_id: str,
            reason_for_change: str,
            new_appointment_timestamp: Optional[datetime],
            new_broker_id: Optional[str]
    ):
        await self.appointment_service.reschedule_appointment(user_id, appointment_id, reason_for_change,
                                                              new_appointment_timestamp, new_broker_id)

    async def get_appointment_details(self, user_id: str, appointment_id: str):
        appt = await self.appointment_service.get_appointment_details(user_id, appointment_id)
        return await self.appointment_service.build_appointment_response(appt)
