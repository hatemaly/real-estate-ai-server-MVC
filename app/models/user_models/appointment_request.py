# src/models/user_models/appointment_request.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.models.user_models.buy_request import RequestStatus


class AppointmentRequest(BaseModel):
    id: Optional[str] = Field(alias="_id")  # MongoDB's primary key
    property_id: List[str] = Field(default_factory=list)
    broker_id: Optional[str] = None
    appointment_timestamp: Optional[datetime] = None
    appointment_location: Optional[str] = None
    minutes_of_meeting: Optional[str] = None
    status: RequestStatus = RequestStatus.PENDING
    request_timestamp: datetime = Field(default_factory=datetime.now)
    customer_feedback: Optional[str] = None
    reason_for_change: Optional[str] = None
    reason_for_rejection: Optional[str] = None
    reason_for_cancellation: Optional[str] = None

    def approve(self, broker_id: str, timestamp: datetime, location: Optional[str] = None):
        self.status = RequestStatus.APPROVED
        self.broker_id = broker_id
        self.appointment_timestamp = timestamp
        self.appointment_location = location

    def reject(self, reason: Optional[str]):
        self.status = RequestStatus.REJECTED
        self.reason_for_rejection = reason

    def cancel(self, reason: Optional[str]):
        self.status = RequestStatus.CANCELLED
        self.reason_for_cancellation = reason

    def update(self, broker_id: str, timestamp: datetime, location: Optional[str] = None, reason: Optional[str] = None):
        self.broker_id = broker_id
        self.appointment_timestamp = timestamp
        self.appointment_location = location
        self.reason_for_change = reason
