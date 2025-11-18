# backend/app/models/delivery_request.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship
from enum import Enum


# Payment status (moved here since order.py was removed)
class PaymentStatus(str, Enum):
    unpaid = "unpaid"
    held = "held"
    released = "released"
    refunded = "refunded"

class DeliveryStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    in_progress = "in_progress"
    delivered = "delivered"
    completed = "completed"
    failed = "failed"

class TaskType(str, Enum):
    parcel = "parcel"
    canteen = "canteen"

class DeliveryTask(Base):
    __tablename__ = "delivery_requests"  # keep existing table name to avoid migrations pain
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # new task type to distinguish parcel vs canteen
    task_type = Column(SAEnum(TaskType), default=TaskType.parcel, nullable=False)

    pickup_location = Column(String, nullable=True)
    dropoff_location = Column(String, nullable=True)

    # payment fields (for canteen / paid deliveries)
    amount = Column(Float, default=0.0)
    payment_status = Column(SAEnum(PaymentStatus), default=PaymentStatus.unpaid, nullable=False)

    status = Column(SAEnum(DeliveryStatus), default=DeliveryStatus.pending, nullable=False)

    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("User", foreign_keys=[customer_id], lazy="joined")
    delivery_user = relationship("User", foreign_keys=[assigned_to], lazy="joined")
# delivery_request model
    held_amount = Column(Float, default=0.0, nullable=False)
    payment_status = Column(SAEnum(PaymentStatus), default=PaymentStatus.unpaid, nullable=False)
    payment_reference = Column(String, nullable=True)  # store simulated txn id
