# src/models/property_models/price.py
from pydantic import  Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from app.models.base_model import BaseModelApp
from app.models.property_models.payment_plan import PaymentPlan


class Price(BaseModelApp):
    amount: Decimal
    currency: str = "EGP"
    price_per_sqm: Optional[float] = None
    payment_plans: List[PaymentPlan] = Field(default_factory=list)
    highlighted_payment_plan: Optional[int] = None
    date_submitted: Optional[datetime] = None
    is_active: bool = True
