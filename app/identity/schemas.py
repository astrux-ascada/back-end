# /app/identity/schemas.py
"""
Esquemas Pydantic para el módulo de Identidad, alineados con el contrato de API
y la nueva estructura de BD granular (RBAC y Sectores).
"""
import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo
from app.core.validation import validate_email, validate_password

# Importar esquemas de otros módulos para anidarlos
from app.sectors.schemas import SectorRead


# --- Esquemas para Permission ---
class PermissionBase(BaseModel):
    name: str = Field(..., example="asset:read")
    description: Optional[str] = Field(None, example="Permite leer la información de los activos.")

class PermissionRead(PermissionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


# --- Esquemas para Role ---
class RoleBase(BaseModel):
    name: str = Field(..., example="Operator")
    description: Optional[str] = Field(None, example="Rol para operadores de planta.")

class RoleCreate(RoleBase):
    permission_ids: List[uuid.UUID] = Field([], description="Lista de IDs de permisos para asignar al rol.")

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[uuid.UUID]] = None

class RoleRead(RoleBase):
    id: uuid.UUID = Field(..., alias="uuid")
    permissions: List[PermissionRead] = []

    class Config:
        from_attributes = True
        populate_by_name = True


# --- Esquemas para User ---
class UserBase(BaseModel):
    email: EmailStr = Field(..., example="operario1@astruxa.com")
    name: Optional[str] = Field(None, example="Juan Pérez")
    avatar_url: Optional[str] = Field(None, alias="avatarUrl", example="https://example.com/avatar.png")

    @field_validator('email', mode='before')
    @classmethod
    def validate_user_email(cls, v: str) -> str:
        if v:
            return validate_email(v)
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role_ids: List[uuid.UUID] = Field([], description="Lista de IDs de roles para asignar al usuario.")
    sector_ids: List[uuid.UUID] = Field([], description="Lista de IDs de sectores a los que el usuario está asignado.")

    @field_validator('password', mode='before')
    @classmethod
    def validate_create_password(cls, v: str, info: ValidationInfo) -> str:
        # Intentamos obtener el email del contexto de validación para evitar que la contraseña lo contenga
        user_context = {}
        if info.data.get('email'):
            user_context['email'] = info.data['email']
        return validate_password(v, user_context)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    role_ids: Optional[List[uuid.UUID]] = None
    sector_ids: Optional[List[uuid.UUID]] = None

    @field_validator('email', mode='before')
    @classmethod
    def validate_update_email(cls, v: str) -> str:
        if v:
            return validate_email(v)
        return v
    
    @field_validator('password', mode='before')
    @classmethod
    def validate_update_password(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        if v:
            user_context = {}
            if info.data.get('email'):
                user_context['email'] = info.data['email']
            return validate_password(v, user_context)
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(UserBase):
    id: uuid.UUID = Field(..., alias="uuid")
    is_active: bool = Field(..., alias="isActive")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    roles: List[RoleRead] = []
    assigned_sectors: List[SectorRead] = Field([], alias="assignedSectors")

    class Config:
        from_attributes = True
        populate_by_name = True


# --- Esquemas para Autenticación ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenWithUser(Token):
    user: UserRead

class TfaToken(BaseModel):
    """Esquema para recibir un token de 2FA."""
    token: str = Field(..., min_length=6, max_length=6, example="123456")
