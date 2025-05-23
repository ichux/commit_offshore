from sqlalchemy import Column, DateTime, Boolean, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import uuid
from datetime import datetime

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    orders = relationship("Order", back_populates="user")
    support_tickets = relationship("SupportTicket", back_populates="user")


class Order(Base, TimestampMixin):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # pending, completed, cancelled

    user = relationship("User", back_populates="orders")
    payments = relationship("Payment", back_populates="order")


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    payment_method = Column(String, nullable=False)
    success = Column(Boolean, nullable=False)

    order = relationship("Order", back_populates="payments")


class SupportTicket(Base, TimestampMixin):
    __tablename__ = "support_tickets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    issue = Column(String, nullable=False)
    resolved = Column(Boolean, default=False)

    user = relationship("User", back_populates="support_tickets")
