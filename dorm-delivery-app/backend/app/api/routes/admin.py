from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.delivery_request import DeliveryTask, DeliveryStatus
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    users_count = db.query(User).count()
    total_deliveries = db.query(DeliveryTask).count()
    active_deliveries = db.query(DeliveryTask).filter(DeliveryTask.status != DeliveryStatus.completed).count()
    pending_deliveries = db.query(DeliveryTask).filter(DeliveryTask.status == DeliveryStatus.pending).count()
    in_progress = db.query(DeliveryTask).filter(DeliveryTask.status == DeliveryStatus.in_progress).count()
    
    # Optional: sum of held/released payments
    total_held = db.query(DeliveryTask).filter(DeliveryTask.payment_status == "held").count()
    
    return {
        "users_count": users_count,
        "total_deliveries": total_deliveries,
        "active_deliveries": active_deliveries,
        "pending_deliveries": pending_deliveries,
        "in_progress": in_progress,
        "total_held_payments": total_held,
    }