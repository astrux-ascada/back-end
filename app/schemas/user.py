# Esquemas Pydantic para el modelo User
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr

from .role import Role


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str
    role_id: uuid.UUID


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[uuid.UUID] = None


class User(UserBase):
    id: uuid.UUID
    is_active: bool
    role: Role

    class Config:
        orm_mode = True
