# /app/identity/schemas.py
"""
Esquemas Pydantic para las entidades User y Role.

Define las formas de los datos para la API, garantizando la validación,
serialización y documentación automática de los endpoints.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# --- Esquemas para Role ---

class RoleBase(BaseModel):
    name: str = Field(..., example="Operator")
    description: Optional[str] = Field(None, example="Standard operator with limited access.")

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


# --- Esquemas para User ---

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="operario1@astruxa.com")
    name: Optional[str] = Field(None, example="Juan Pérez")
    username: Optional[str] = Field(None, example="jperez")
    phone: Optional[str] = Field(None, example="+34600123456")
    position: Optional[str] = Field(None, example="Líder de Turno")
    occupation: Optional[str] = Field(None, example="Mecánico de Mantenimiento")
    avatar_url: Optional[str] = Field(None, example="https://example.com/avatar.png")
    preferred_language: str = Field("es", example="es")
    employee_id: Optional[str] = Field(None, example="E-12345")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="secure_password_123")
    role_id: Optional[uuid.UUID] = Field(None, description="ID of the role to assign to the user.")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="operario1@astruxa.com")
    password: str = Field(..., example="secure_password_123")


class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    role: Optional[RoleRead] = None  # Relación anidada con el rol

    class Config:
        from_attributes = True


# --- Esquemas para Autenticación ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenWithUser(Token):
    user: UserRead
