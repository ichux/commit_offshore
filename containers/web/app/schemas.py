from pydantic import BaseModel, UUID4, ConfigDict
from datetime import datetime
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    email: str


class User(UserBase):
    id: UUID4
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    amount: float
    status: str


class Order(OrderBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentBase(BaseModel):
    payment_method: str
    success: bool


class Payment(PaymentBase):
    id: UUID4
    order_id: UUID4
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SupportTicketBase(BaseModel):
    issue: str
    resolved: bool


class SupportTicket(SupportTicketBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TotalSpent(BaseModel):
    user_id: UUID4
    total_spent: float

    model_config = ConfigDict(from_attributes=True)


class UserOrderStats(BaseModel):
    user_id: UUID4
    first_order_date: Optional[datetime]
    total_orders: int
    has_support_ticket: bool

    model_config = ConfigDict(from_attributes=True)
