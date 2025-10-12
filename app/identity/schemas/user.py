# /app/identity/schemas/user.py
"""
Esquemas de Pydantic para la entidad User.
"""

import uuid
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# --- Esquema Base ---
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    occupation: Optional[str] = None
    preferred_language: str = "es"
    employee_id: Optional[str] = None

# --- Esquema para Creación ---
class UserCreate(UserBase):
    password: str
    role_ids: Optional[List[uuid.UUID]] = []
    sector_ids: Optional[List[uuid.UUID]] = []

# --- Esquema para Actualización ---
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    occupation: Optional[str] = None
    preferred_language: Optional[str] = None
    is_active: Optional[bool] = None
    role_ids: Optional[List[uuid.UUID]] = None
    sector_ids: Optional[List[uuid.UUID]] = None

# --- Esquema para Lectura ---
class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True
