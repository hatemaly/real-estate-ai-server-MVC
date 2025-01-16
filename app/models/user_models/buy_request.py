# src/models/user_models/buy_request.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    CHANGED = "changed"


class BuyRequest(BaseModel):
    id: Optional[str] = Field(alias="_id")  # MongoDB's primary key
    property_id: List[str] = Field(default_factory=list)
    broker_id: Optional[str] = None
    status: RequestStatus = RequestStatus.PENDING
    request_timestamp: datetime = Field(default_factory=datetime.now)
    deal_timestamp: Optional[datetime] = None
    reason_for_change: Optional[str] = None
    reason_for_rejection: Optional[str] = None
    reason_for_cancellation: Optional[str] = None
    deal_feedback: Optional[str] = None

    def approve(self, broker_id: str, deal_timestamp: datetime):
        self.status = RequestStatus.APPROVED
        self.deal_timestamp = deal_timestamp
        self.broker_id = broker_id

    def reject(self, reason: str):
        self.status = RequestStatus.REJECTED
        self.reason_for_rejection = reason

    def cancel(self, reason: str):
        self.status = RequestStatus.CANCELLED
        self.reason_for_cancellation = reason

    def update(self, new_timestamp: datetime, new_broker_id: str, reason: Optional[str] = None):
        self.deal_timestamp = new_timestamp
        self.broker_id = new_broker_id
        self.reason_for_change = reason
