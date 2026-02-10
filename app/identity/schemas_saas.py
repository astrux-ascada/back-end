# /app/identity/schemas_saas.py
"""
Esquemas Pydantic para la gestión del modelo de negocio SaaS.
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, EmailStr

# --- Esquemas para Plan ---

class PlanBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=100)
    price_monthly: float = Field(..., ge=0)
    price_yearly: float = Field(..., ge=0)
    currency: str = Field("USD", max_length=3)
    limits: Optional[Dict[str, Any]] = {}
    features: Optional[Dict[str, Any]] = {}
    is_active: bool = True

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    name: Optional[str] = None
    price_monthly: Optional[float] = None
    price_yearly: Optional[float] = None
    currency: Optional[str] = None
    limits: Optional[Dict[str, Any]] = None
    features: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class PlanRead(PlanBase):
    id: uuid.UUID
    class Config:
        from_attributes = True

# --- Esquemas para Tenant ---

class TenantBase(BaseModel):
    name: str = Field(..., max_length=100)
    logo_url: Optional[str] = Field(None, description="URL del logo de la empresa.")
    website: Optional[str] = Field(None, description="Sitio web de la empresa.")
    tax_id: Optional[str] = Field(None, description="Identificador fiscal (CIF, NIF, VAT ID).")
    billing_address: Optional[str] = Field(None, description="Dirección de facturación.")
    contact_email: Optional[EmailStr] = Field(None, description="Email central para notificaciones.")
    contact_phone: Optional[str] = Field(None, description="Teléfono de contacto principal.")
    timezone: str = Field("UTC", description="Zona horaria del tenant (ej: 'Europe/Madrid').")
    language: str = Field("es", description="Idioma preferido (ej: 'es', 'en').")
    currency: str = Field("USD", description="Moneda por defecto (ej: 'USD', 'EUR').")
    config: Optional[Dict[str, Any]] = Field({}, description="Configuración flexible en formato JSON.")
    is_active: bool = True

class TenantCreate(TenantBase):
    slug: str
    partner_id: Optional[uuid.UUID] = None

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    tax_id: Optional[str] = None
    billing_address: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    currency: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class TenantRead(TenantBase):
    id: uuid.UUID
    slug: str
    deleted_at: Optional[datetime] = None
    account_manager_id: Optional[uuid.UUID] = None
    class Config:
        from_attributes = True

class TenantDeletionRequest(BaseModel):
    justification: str = Field(..., min_length=10, description="Justificación detallada para la solicitud de borrado.")

class TenantDeletionConfirmation(BaseModel):
    confirmation_key: str = Field(..., description="Clave de confirmación requerida para el borrado.")

class TenantManagerAssignment(BaseModel):
    account_manager_id: uuid.UUID = Field(..., description="ID del usuario (PLATFORM_ADMIN) a asignar como gestor de cuenta.")

# --- Esquemas para Suscripción ---

class SubscriptionBase(BaseModel):
    plan_id: uuid.UUID

class SubscriptionUpdate(SubscriptionBase):
    pass

class SubscriptionRead(SubscriptionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: str
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    class Config:
        from_attributes = True

# --- Esquema para Registro Público ---

class PublicRegistrationRequest(BaseModel):
    company_name: str = Field(..., min_length=2)
    admin_name: str = Field(..., min_length=2)
    admin_email: EmailStr
    admin_password: str = Field(..., min_length=8)
    plan_id: uuid.UUID

# --- Esquema para Reporte de Uso ---

class UsageDetail(BaseModel):
    used: int
    limit: int

class UsageReport(BaseModel):
    users: UsageDetail
    assets: UsageDetail

# --- Esquemas para Partners ---

class PartnerTenantRead(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    subscription_status: str
    plan_name: str

class CommissionRead(BaseModel):
    tenant_name: str
    amount: float
    currency: str
    date: datetime
    status: str
