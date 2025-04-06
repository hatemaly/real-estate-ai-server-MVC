# app/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime

from app.controllers.user_controller import UserController
from app.controllers.appointment_controller import AppointmentController
from app.repositories.user_repository import UserRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.database.collections import get_user_collection, get_appointment_collection
from app.services.user_service import UserService
from app.services.appointment_service import AppointmentService
from app.models.user_models.user import User
from app.models.user_models.appointment_request import AppointmentType, RequestStatus

router = APIRouter()


async def get_user_controller() -> UserController:
    user_collection = await get_user_collection()
    user_repository = UserRepository(user_collection)
    user_service = UserService(user_repository)
    return UserController(user_service)


async def get_appointment_controller() -> AppointmentController:
    # 1) التهيئة
    appt_collection = await get_appointment_collection()
    appt_repo = AppointmentRepository(appt_collection)

    user_collection = await get_user_collection()
    user_repository = UserRepository(user_collection)
    user_service = UserService(user_repository)

    # property_collection = ... (إن وجد)
    # property_service = PropertyService(...)

    # 2) انشاء الـservice ثم الـcontroller
    appt_service = AppointmentService(
        appointment_repository=appt_repo,
        property_service=None,  # أو property_service
        user_service=user_service
    )
    return AppointmentController(appt_service)


# ------------------------------------------------------------------------------
# مَسارات المستخدم الأساسية (قديمة) ...
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# مَسارات المواعيد الخاصة بالمستخدم (/me/appointments)
# ------------------------------------------------------------------------------
@router.get("/me/appointments")
async def get_appointments(
        appointment_type: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
        appointment_controller: AppointmentController = Depends(get_appointment_controller),
        current_user_id: str = Depends(...),
):
    """
    GET /api/v1/users/me/appointments?appointment_type=?&status=?&page=?&limit=?
    """
    try:
        return await appointment_controller.get_appointments(
            user_id=current_user_id,
            appointment_type=appointment_type,
            status=status,
            page=page,
            limit=limit
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/me/appointments")
async def create_appointment(
        property_ids: List[str],
        appointment_type: Optional[str] = None,
        appointment_controller: AppointmentController = Depends(get_appointment_controller),
        current_user_id: str = Depends(...),
):
    """
    POST /api/v1/users/me/appointments
    body: { "property_ids": [...], "appointment_type": "..." }
    """
    return await appointment_controller.create_appointment(current_user_id, property_ids, appointment_type)


@router.put("/me/appointments/{appointment_id}/approve")
async def approve_appointment(
        appointment_id: str,
        broker_id: str,
        appointment_timestamp: datetime,
        appointment_controller: AppointmentController = Depends(get_appointment_controller),
        current_user_id: str = Depends(...),
):
    """
    PUT /api/v1/users/me/appointments/{id}/approve
    body: { "appointment_timestamp": "2025-01-01T10:00:00", "broker_id": "someBrokerId" }
    """
    await appointment_controller.approve_appointment(
        current_user_id,
        appointment_id,
        broker_id,
        appointment_timestamp
    )
    return {"success": True}


@router.put("/me/appointments/{appointment_id}/reject")
async def reject_appointment(
        appointment_id: str,
        reason_for_rejection: str,
        appointment_controller: AppointmentController = Depends(get_appointment_controller),
        current_user_id: str = Depends(...),
):
    """
    PUT /api/v1/users/me/appointments/{id}/reject
    body: { "reason_for_rejection": "some reason" }
    """
    await appointment_controller.reject_appointment(current_user_id, appointment_id, reason_for_rejection)
    return {"success": True}


@router.put("/me/appointments/{appointment_id}/cancel")
async def cancel_appointment(
        appointment_id: str,
        reason_for_cancellation: str,
        appointment_controller: AppointmentController = Depends(get_appointment_controller),
        current_user_id: str = Depends(...),
):
    """
    PUT /api/v1/users/me/appointments/{id}/cancel
    body: { "reason_for_cancellation": "some reason" }
    """
    await appointment_controller.cancel_appointment(current_user_id, appointment_id, reason_for_cancellation)
    return {"success": True}


@router.put("/me/appointments/{appointment_id}/fullfilled")
async def fulfill_appointment(
        appointment_id: str,
        moms: str,
        broker_id: Optional[str] = None,
        appointment_timestamp: Optional[datetime] = None,
        appointment_controller: AppointmentController = Depends(get_appointment_controller),
        current_user_id: str = Depends(...),
):
    """
    PUT /api/v1/users/me/appointments/{id}/fullfilled
    body: { "moms": "...", "broker_id"?: "", "appointment_timestamp"?: "..." }
    """
    await appointment_controller.fulfill_appointment(current_user_id, appointment_id, moms, broker_id,
                                                     appointment_timestamp)
    return {"success": True}


@router.put("/me/appointments/{appointment_id}/reschedule")
async def reschedule_appointment(
        appointment_id: str,
        reason_for_change: str,
        new_appointment_timestamp: Optional[datetime] = None,
        new_broker_id: Optional[str] = None,
        appointment_controller: AppointmentController = Depends(get_appointment_controller),
        current_user_id: str = Depends(...),
):
    """
    PUT /api/v1/users/me/appointments/{id}/reschedule
    body: { "reason_for_change": "...", "new_appointment_timestamp"?: "...", "new_broker_id"?: "..." }
    """
    await appointment_controller.reschedule_appointment(
        current_user_id,
        appointment_id,
        reason_for_change,
        new_appointment_timestamp,
        new_broker_id
    )
    return {"success": True}


@router.get("/me/appointments/{appointment_id}")
async def get_appointment(
        appointment_id: str,
        appointment_controller: AppointmentController = Depends(get_appointment_controller),
        current_user_id: str = Depends(...),
):
    """
    GET /api/v1/users/me/appointments/{id}
    """
    try:
        return await appointment_controller.get_appointment_details(current_user_id, appointment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
