# /app/identity/schemas.py
"""
Esquemas Pydantic para la gestión de usuarios y roles.
"""
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# --- Esquemas Auxiliares ---

class TenantSimple(BaseModel):
    """Representación ligera de un Tenant para anidar en respuestas."""
    id: uuid.UUID
    name: str
    slug: str
    
    class Config:
        from_attributes = True

class SectorSimple(BaseModel):
    """Representación ligera de un Sector (Área de Planta)."""
    id: uuid.UUID
    name: str
    code: str
    
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
    permissions: List[PermissionRead] = []

    class Config:
        from_attributes = True

# --- Esquemas para User (Nivel Tenant) ---

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    is_active: bool = True
    # Campos de perfil extendido
    job_title: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role_ids: List[uuid.UUID] = []
    sector_ids: List[uuid.UUID] = [] # Asignación de áreas

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)
    role_ids: Optional[List[uuid.UUID]] = None
    sector_ids: Optional[List[uuid.UUID]] = None
    job_title: Optional[str] = None
    phone_number: Optional[str] = None

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_tfa_enabled: bool
    
    # Campos enriquecidos (Relaciones)
    roles: List[RoleRead] = []
    tenant: Optional[TenantSimple] = None
    assigned_sectors: List[SectorSimple] = [] # Sectores asignados
    
    class Config:
        from_attributes = True

# --- Esquemas para User (Nivel Sistema/Global) ---

class UserCreateSys(BaseModel):
    """Schema para crear un usuario desde el panel de sistema."""
    email: EmailStr
    name: str
    password: str = Field(..., min_length=8)
    tenant_id: Optional[uuid.UUID] = None
    role_ids: List[uuid.UUID] = []
    sector_ids: List[uuid.UUID] = []
    is_active: bool = True
    job_title: Optional[str] = None
    phone_number: Optional[str] = None

class UserUpdateSys(BaseModel):
    """Schema para actualizar un usuario desde el panel de sistema."""
    name: Optional[str] = None
    is_active: Optional[bool] = None
    tenant_id: Optional[uuid.UUID] = None
    role_ids: Optional[List[uuid.UUID]] = None
    sector_ids: Optional[List[uuid.UUID]] = None
    job_title: Optional[str] = None
    phone_number: Optional[str] = None

# --- Esquemas de Autenticación ---

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
