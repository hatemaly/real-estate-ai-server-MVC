# app/services/appointment_service.py
from typing import Optional, List
from datetime import datetime

from app.repositories.appointment_repository import AppointmentRepository
from app.models.user_models.appointment_request import (
    AppointmentRequest,
    AppointmentType,
    RequestStatus
)


class AppointmentService:
    def __init__(
            self,
            appointment_repository: AppointmentRepository,
            property_service,  # لوصول معلومات العقار
            user_service  # لجلب بيانات broker
    ):
        self.appointment_repository = appointment_repository
        self.property_service = property_service
        self.user_service = user_service

    async def get_appointments(
            self,
            user_id: str,
            appointment_type: Optional[str],
            status: Optional[str],
            page: int = 1,
            limit: int = 10
    ):
        skip = (page - 1) * limit
        items = await self.appointment_repository.find_appointments(
            customer_id=user_id,
            appointment_type=appointment_type,
            status=status,
            skip=skip,
            limit=limit
        )
        total = await self.appointment_repository.count_appointments(
            customer_id=user_id,
            appointment_type=appointment_type,
            status=status
        )
        return items, total

    async def create_appointment(self, user_id: str, property_ids: List[str], appointment_type: Optional[str]):
        # إنشاء كائن AppointmentRequest جديد
        appointment = AppointmentRequest(
            customer_id=user_id,
            property_id=property_ids,
            appointment_type=AppointmentType(appointment_type) if appointment_type else AppointmentType.VISIT,
            status=RequestStatus.PENDING
        )
        await self.appointment_repository.save(appointment)
        return appointment

    async def approve_appointment(self, user_id: str, appointment_id: str, broker_id: str, timestamp: datetime):
        appt = await self.appointment_repository.get_by_id_and_customer(appointment_id, user_id)
        if not appt:
            raise ValueError("Appointment not found or not authorized")

        appt.approve(broker_id, timestamp)
        await self.appointment_repository.update(appt)

    async def reject_appointment(self, user_id: str, appointment_id: str, reason: str):
        appt = await self.appointment_repository.get_by_id_and_customer(appointment_id, user_id)
        if not appt:
            raise ValueError("Appointment not found or not authorized")

        appt.reject(reason)
        await self.appointment_repository.update(appt)

    async def cancel_appointment(self, user_id: str, appointment_id: str, reason: str):
        appt = await self.appointment_repository.get_by_id_and_customer(appointment_id, user_id)
        if not appt:
            raise ValueError("Appointment not found or not authorized")

        appt.cancel(reason)
        await self.appointment_repository.update(appt)

    async def fulfill_appointment(
            self,
            user_id: str,
            appointment_id: str,
            moms: str,
            broker_id: Optional[str] = None,
            timestamp: Optional[datetime] = None
    ):
        appt = await self.appointment_repository.get_by_id_and_customer(appointment_id, user_id)
        if not appt:
            raise ValueError("Appointment not found or not authorized")

        appt.fulfill(moms, broker_id, timestamp)
        await self.appointment_repository.update(appt)

    async def reschedule_appointment(
            self,
            user_id: str,
            appointment_id: str,
            reason_for_change: str,
            new_appointment_timestamp: Optional[datetime] = None,
            new_broker_id: Optional[str] = None
    ):
        appt = await self.appointment_repository.get_by_id_and_customer(appointment_id, user_id)
        if not appt:
            raise ValueError("Appointment not found or not authorized")

        appt.update(
            broker_id=new_broker_id,
            timestamp=new_appointment_timestamp,
            reason=reason_for_change
        )

        appt.status = RequestStatus.CHANGED
        await self.appointment_repository.update(appt)

    async def get_appointment_details(self, user_id: str, appointment_id: str) -> AppointmentRequest:
        appt = await self.appointment_repository.get_by_id_and_customer(appointment_id, user_id)
        if not appt:
            raise ValueError("Appointment not found or not authorized")
        return appt

    async def build_appointment_response(self, appt: AppointmentRequest):

        property_list = []
        for prop_id in appt.property_id:
            prop_doc = await self.property_service.get_property_by_id(prop_id)
            if prop_doc:
                property_list.append({
                    "id": prop_doc.id,
                    "title": prop_doc.title,
                    "price": prop_doc.price
                })

        # 2) جلب بيانات الوسيط (broker)
        broker_data = None
        if appt.broker_id:
            broker_user = await self.user_service.get_user_by_id(appt.broker_id)
            if broker_user:
                broker_data = {
                    "id": broker_user.id,
                    "name": broker_user.full_name
                }

        response_dict = {
            "id": appt.id,
            "properties": property_list,
            "appointment_type": appt.appointment_type,
            "status": appt.status,
            "broker": broker_data,
            "request_timestamp": appt.request_timestamp,
            "appointment_timestamp": appt.appointment_timestamp,
            "reason_for_change": appt.reason_for_change,
            "reason_for_rejection": appt.reason_for_rejection,
            "reason_for_cancellation": appt.reason_for_cancellation,
            "moms": appt.minutes_of_meeting  # إن أردت إرجاع minutes_of_meeting باسم moms
        }
        return response_dict
