# src/models/user_models/buy_request.py
# This module defines models for managing property purchase requests.
# It includes status tracking and methods to handle the lifecycle of a buy request.

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RequestStatus(str, Enum):
    """
    Enumeration for tracking the status of requests.
    
    These status values are used for both buy requests and appointment requests
    to track their progress through the system.
    
    Values:
        PENDING: Request has been submitted but not yet processed
        APPROVED: Request has been approved by a broker
        REJECTED: Request has been rejected by a broker
        CANCELLED: Request has been cancelled by the user
        CHANGED: Request details have been modified
    """
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    CHANGED = "changed"


class BuyRequest(BaseModel):
    """
    Model for tracking property purchase requests.
    
    This model represents a user's request to purchase one or more properties,
    and includes the complete lifecycle of the request from submission to completion.
    
    Attributes:
        id: Unique identifier for the request (MongoDB ObjectId)
        property_id: List of property identifiers the user wants to purchase
        broker_id: Identifier of the broker handling this purchase request
        status: Current status of the buy request
        request_timestamp: When the purchase request was initially submitted
        deal_timestamp: When the purchase deal was finalized (if approved)
        reason_for_change: Explanation for any changes to the request
        reason_for_rejection: Explanation if the request was rejected
        reason_for_cancellation: Explanation if the request was cancelled
        deal_feedback: Feedback about the purchase deal process
    """
    id: Optional[str] = Field(alias="_id")  # MongoDB's primary key
    property_id: List[str] = Field(default_factory=list)  # List of property IDs to purchase
    broker_id: Optional[str] = None  # ID of assigned broker
    status: RequestStatus = RequestStatus.PENDING  # Current status
    request_timestamp: datetime = Field(default_factory=datetime.now)  # When request was created
    deal_timestamp: Optional[datetime] = None  # When deal was finalized (if approved)
    reason_for_change: Optional[str] = None  # Reason if request details changed
    reason_for_rejection: Optional[str] = None  # Reason if request was rejected
    reason_for_cancellation: Optional[str] = None  # Reason if request was cancelled
    deal_feedback: Optional[str] = None  # Feedback about the purchase process

    def approve(self, broker_id: str, deal_timestamp: datetime):
        """
        Approve the buy request.
        
        Args:
            broker_id: ID of the broker approving the request
            deal_timestamp: When the deal was or will be finalized
        """
        self.status = RequestStatus.APPROVED
        self.deal_timestamp = deal_timestamp
        self.broker_id = broker_id

    def reject(self, reason: str):
        """
        Reject the buy request.
        
        Args:
            reason: Explanation for why the request was rejected
        """
        self.status = RequestStatus.REJECTED
        self.reason_for_rejection = reason

    def cancel(self, reason: str):
        """
        Cancel the buy request.
        
        Args:
            reason: Explanation for why the request was cancelled
        """
        self.status = RequestStatus.CANCELLED
        self.reason_for_cancellation = reason

    def update(self, new_timestamp: datetime, new_broker_id: str, reason: Optional[str] = None):
        """
        Update the buy request details.
        
        Args:
            new_timestamp: New timestamp for when the deal will be finalized
            new_broker_id: New broker ID assigned to the request
            reason: Explanation for why the request was updated
        """
        self.deal_timestamp = new_timestamp
        self.broker_id = new_broker_id
        self.reason_for_change = reason
