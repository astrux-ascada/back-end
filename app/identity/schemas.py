# /app/identity/schemas.py
"""
Esquemas Pydantic para la gestión de usuarios y roles.
"""
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# --- Esquemas para User ---

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role_ids: List[uuid.UUID] = []

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)
    role_ids: Optional[List[uuid.UUID]] = None

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_tfa_enabled: bool
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenWithUser(Token):
    user: UserRead

class TfaToken(BaseModel):
    token: str = Field(..., min_length=6, max_length=6)

# --- Esquemas para Role ---

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: List[uuid.UUID] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[uuid.UUID]] = None

class RoleRead(RoleBase):
    id: uuid.UUID
    permissions: List['PermissionRead'] = []

    class Config:
        from_attributes = True

# --- Esquemas para Permission ---

class PermissionBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None

class PermissionRead(PermissionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# Actualizar la referencia forward para RoleRead
RoleRead.model_rebuild()
