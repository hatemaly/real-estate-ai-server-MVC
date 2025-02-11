# app/models/user_models/appointment_request.py

from pydantic import  Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.models.base_model import BaseModelApp
from app.models.user_models.buy_request import RequestStatus


class AppointmentType(str, Enum):
    BUY = "Buy"
    INSPECTION = "Inspection"


class AppointmentRequest(BaseModelApp):

    property_id: List[str] = Field(default_factory=list)
    broker_id: Optional[str] = None

    appointment_type: Optional[AppointmentType] = AppointmentType.VISIT

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

    def update(
            self,
            broker_id: Optional[str] = None,
            timestamp: Optional[datetime] = None,
            location: Optional[str] = None,
            reason: Optional[str] = None
    ):
        if broker_id:
            self.broker_id = broker_id
        if timestamp:
            self.appointment_timestamp = timestamp
        if location:
            self.appointment_location = location
        self.reason_for_change = reason

    def fulfill(self, moms: str, broker_id: Optional[str] = None, timestamp: Optional[datetime] = None):
        self.minutes_of_meeting = moms
        if broker_id:
            self.broker_id = broker_id
        if timestamp:
            self.appointment_timestamp = timestamp

        self.status = RequestStatus.CHANGED
