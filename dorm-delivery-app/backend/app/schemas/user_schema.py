from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import RoleEnum

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    rating: float

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"