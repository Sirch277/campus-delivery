# backend/app/services/delivery_service.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.delivery_request import DeliveryTask, DeliveryStatus

def create_task(db: Session, customer_id: int, payload) -> DeliveryTask:
    task = DeliveryTask(
        title=payload.title,
        description=payload.description,
        task_type=getattr(payload, "task_type", DeliveryTask.task_type.default),  # payload may include type
        pickup_location=getattr(payload, "pickup_location", None),
        dropoff_location=getattr(payload, "dropoff_location", None),
        amount=getattr(payload, "amount", 0.0),
        customer_id=customer_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def list_available_deliveries(db: Session) -> List[DeliveryTask]:
    return db.query(DeliveryTask).filter(DeliveryTask.status == DeliveryStatus.pending).all()

def get_delivery(db: Session, delivery_id: int) -> Optional[DeliveryTask]:
    return db.query(DeliveryTask).filter(DeliveryTask.id == delivery_id).first()

def accept_delivery(db: Session, delivery: DeliveryTask, delivery_user_id: int) -> DeliveryTask:
    delivery.status = DeliveryStatus.accepted
    delivery.assigned_to = delivery_user_id
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    return delivery

def update_status(db: Session, dr: DeliveryTask, status: DeliveryStatus) -> DeliveryTask:
    dr.status = status
    db.commit()
    db.refresh(dr)
    return dr

def complete_delivery(db: Session, delivery: DeliveryTask) -> DeliveryTask:
    delivery.status = DeliveryStatus.completed
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    return delivery

def list_by_customer(db: Session, customer_id: int) -> List[DeliveryTask]:
    return db.query(DeliveryTask).filter(DeliveryTask.customer_id == customer_id).all()

def list_by_assigned(db: Session, user_id: int) -> List[DeliveryTask]:
    return db.query(DeliveryTask).filter(DeliveryTask.assigned_to == user_id).all()
