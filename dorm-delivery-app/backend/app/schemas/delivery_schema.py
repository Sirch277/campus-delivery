# backend/app/schemas/delivery_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.delivery_request import DeliveryStatus, TaskType, PaymentStatus

class DeliveryCreate(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: Optional[TaskType] = TaskType.parcel
    pickup_location: Optional[str] = None
    dropoff_location: Optional[str] = None
    amount: Optional[float] = 0.0

class DeliveryOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    task_type: TaskType
    pickup_location: Optional[str]
    dropoff_location: Optional[str]
    amount: float
    payment_status: PaymentStatus
    status: DeliveryStatus
    customer_id: int
    assigned_to: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
