# src/models/property_models/payment_plan.py
from pydantic import  Field
from typing import List, Optional
from enum import Enum
from decimal import Decimal

from app.models.base_model import BaseModelApp


class InstallmentType(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class SpecialPayment(BaseModelApp):
    name: str
    event_month: Optional[int] = None  # Month number of the payment
    amount: Optional[Decimal] = None
    percentage: Optional[float] = None
    description: Optional[str] = None


class PaymentPlan(BaseModelApp):
    id: Optional[str] = None  # MongoDB or UUID
    name: str   
    description: Optional[str] = None
    down_payment_percentage: Optional[float] = None
    installment_years: Optional[int] = None
    installment_amount: Optional[Decimal] = None
    installment_type: Optional[InstallmentType] = None
    special_payments: List[SpecialPayment] = Field(default_factory=list)
    interest_rate: Optional[float] = None
    discount_percentage: Optional[float] = None
    discount_amount: Optional[Decimal] = None
    is_active: bool = True
