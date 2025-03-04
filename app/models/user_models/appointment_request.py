# src/models/user_models/appointment_request.py
# This module defines the model for handling property viewing appointment requests.
# It includes status tracking, scheduling information, and methods to manage the lifecycle of an appointment.

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.models.user_models.buy_request import RequestStatus


class AppointmentRequest(BaseModel):
    """
    Model for managing property viewing appointment requests between users and brokers.
    
    This model tracks the entire lifecycle of an appointment request including scheduling,
    approval, rejection, cancellation, and feedback.
    
    Attributes:
        id: Unique identifier for the appointment request (MongoDB ObjectId)
        property_id: List of property identifiers associated with this appointment
        broker_id: Identifier of the broker assigned to this appointment
        appointment_timestamp: Scheduled date and time for the appointment
        appointment_location: Location where the appointment will take place
        minutes_of_meeting: Notes or summary from the meeting
        status: Current status of the appointment request
        request_timestamp: When the appointment was initially requested
        customer_feedback: Feedback provided by the customer after the appointment
        reason_for_change: Explanation for any changes to the appointment
        reason_for_rejection: Explanation if the appointment was rejected
        reason_for_cancellation: Explanation if the appointment was cancelled
    """
    id: Optional[str] = Field(alias="_id")  # MongoDB's primary key
    property_id: List[str] = Field(default_factory=list)  # List of property IDs to view
    broker_id: Optional[str] = None  # ID of the broker assigned to this appointment
    appointment_timestamp: Optional[datetime] = None  # Scheduled time for the appointment
    appointment_location: Optional[str] = None  # Where the appointment will take place
    minutes_of_meeting: Optional[str] = None  # Notes from the meeting
    status: RequestStatus = RequestStatus.PENDING  # Current status of the request
    request_timestamp: datetime = Field(default_factory=datetime.now)  # When request was created
    customer_feedback: Optional[str] = None  # Feedback after the appointment
    reason_for_change: Optional[str] = None  # Reason if appointment details changed
    reason_for_rejection: Optional[str] = None  # Reason if appointment was rejected
    reason_for_cancellation: Optional[str] = None  # Reason if appointment was cancelled

    def approve(self, broker_id: str, timestamp: datetime, location: Optional[str] = None):
        """
        Approve the appointment request.
        
        Args:
            broker_id: ID of the broker approving the request
            timestamp: Scheduled date and time for the appointment
            location: Location where the appointment will take place
        """
        self.status = RequestStatus.APPROVED
        self.broker_id = broker_id
        self.appointment_timestamp = timestamp
        self.appointment_location = location

    def reject(self, reason: Optional[str]):
        """
        Reject the appointment request.
        
        Args:
            reason: Explanation for why the request was rejected
        """
        self.status = RequestStatus.REJECTED
        self.reason_for_rejection = reason

    def cancel(self, reason: Optional[str]):
        """
        Cancel the appointment request.
        
        Args:
            reason: Explanation for why the request was cancelled
        """
        self.status = RequestStatus.CANCELLED
        self.reason_for_cancellation = reason

    def update(self, broker_id: str, timestamp: datetime, location: Optional[str] = None, reason: Optional[str] = None):
        """
        Update the appointment request details.
        
        Args:
            broker_id: New broker ID for the appointment
            timestamp: New date and time for the appointment
            location: New location for the appointment
            reason: Explanation for why the appointment was updated
        """
        self.broker_id = broker_id
        self.appointment_timestamp = timestamp
        self.appointment_location = location
        self.reason_for_change = reason
