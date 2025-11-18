# backend/app/api/routes/deliveries.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.delivery_schema import DeliveryCreate, DeliveryOut
from app.models.delivery_request import DeliveryTask, DeliveryStatus, PaymentStatus
from app.api.deps import get_current_user
from app.services import delivery_service, payment_service


router = APIRouter()

# Create a new delivery task (customer)
@router.post("/", response_model=DeliveryOut)
def create_delivery(payload: DeliveryCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role.value != "customer":
        raise HTTPException(status_code=403, detail="Only customers can create delivery requests")
    dr = delivery_service.create_task(db, current_user.id, payload)
    return dr

# List tasks available for delivery users
@router.get("/available-tasks", response_model=List[DeliveryOut])
def available_tasks(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role.value != "delivery":
        raise HTTPException(status_code=403, detail="Only delivery users can view available tasks")
    return delivery_service.list_available_deliveries(db)

# List tasks created by current customer
@router.get("/", response_model=List[DeliveryOut])
def list_my_deliveries(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delivery_service.list_by_customer(db, current_user.id)

# List tasks assigned to current delivery user
@router.get("/my", response_model=List[DeliveryOut])
def my_assigned(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delivery_service.list_by_assigned(db, current_user.id)

# Accept (claim) a task
@router.post("/{delivery_id}/accept", response_model=DeliveryOut)
def accept_delivery(delivery_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role.value != "delivery":
        raise HTTPException(status_code=403, detail="Only delivery users can accept tasks")
    dr = delivery_service.get_delivery(db, delivery_id)
    if not dr:
        raise HTTPException(status_code=404, detail="Not found")
    if dr.status != DeliveryStatus.pending:
        raise HTTPException(status_code=400, detail="Task not available")
    dr = delivery_service.accept_delivery(db, dr, current_user.id)
    return dr

# Mark as in-progress
@router.post("/{delivery_id}/start", response_model=DeliveryOut)
def start_delivery(delivery_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    dr = delivery_service.get_delivery(db, delivery_id)
    if not dr:
        raise HTTPException(status_code=404, detail="Not found")
    if dr.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not assigned to you")
    dr = delivery_service.update_status(db, dr, DeliveryStatus.in_progress)
    return dr

# Delivery person marks delivered
@router.post("/{delivery_id}/mark-delivered", response_model=DeliveryOut)
def mark_delivered(delivery_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    dr = delivery_service.get_delivery(db, delivery_id)
    if not dr:
        raise HTTPException(status_code=404, detail="Not found")
    if dr.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not assigned to you")
    dr = delivery_service.update_status(db, dr, DeliveryStatus.delivered)
    return dr

# Delivery person fails/cancels task
@router.post("/{delivery_id}/fail", response_model=DeliveryOut)
def fail_delivery(delivery_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    dr = delivery_service.get_delivery(db, delivery_id)
    if not dr:
        raise HTTPException(status_code=404, detail="Not found")
    if dr.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not assigned to you")
    dr = delivery_service.update_status(db, dr, DeliveryStatus.failed)
    return dr

@router.post("/{delivery_id}/confirm", response_model=DeliveryOut)
def confirm_delivery(delivery_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Customer confirms successful delivery."""
    dr = delivery_service.get_delivery(db, delivery_id)
    if not dr:
        raise HTTPException(status_code=404, detail="Not found")
    if dr.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your delivery")
    if dr.status != DeliveryStatus.delivered:
        raise HTTPException(status_code=400, detail="Delivery not yet marked delivered")
    dr = delivery_service.update_status(db, dr, DeliveryStatus.completed)
    return dr
# create a payment intent (simulate)
@router.post("/{delivery_id}/pay")
def pay_for_delivery(delivery_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    dr = delivery_service.get_delivery(db, delivery_id)
    if not dr or dr.customer_id != current_user.id:
        raise HTTPException(404)
    if dr.payment_status != PaymentStatus.unpaid:
        raise HTTPException(400, "Already paid")
    # simulate charge: set held_amount and payment_status=held
    payment_ref = payment_service.simulate_charge(db, dr.id, amount=dr.amount)
    dr.held_amount = dr.amount
    dr.payment_reference = payment_ref
    dr.payment_status = PaymentStatus.held
    db.commit(); db.refresh(dr)
    return {"status":"held","payment_reference":payment_ref}

# customer confirms -> release funds (simulate)
@router.post("/{delivery_id}/release")
def release_payment(delivery_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    dr = delivery_service.get_delivery(db, delivery_id)
    if not dr or dr.customer_id != current_user.id:
        raise HTTPException(404)
    if dr.status != DeliveryStatus.delivered:
        raise HTTPException(400, "Driver hasn't marked delivered yet")
    if dr.payment_status != PaymentStatus.held:
        raise HTTPException(400, "No held funds")
    payment_service.simulate_release(db, dr.payment_reference)
    dr.payment_status = PaymentStatus.released
    db.commit(); db.refresh(dr)
    return dr
