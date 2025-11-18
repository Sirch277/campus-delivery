from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.user_schema import UserOut

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_me(current_user = Depends(get_current_user)):
    return current_user