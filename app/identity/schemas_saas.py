# /app/identity/schemas_saas.py
"""
Esquemas Pydantic para la gestión del modelo de negocio SaaS (Planes, Tenants, Suscripciones).
"""
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, field_validator, EmailStr

from app.identity.models.saas.tenant import TenantStatus
from app.identity.models.saas.subscription import SubscriptionStatus

# --- PLANES (PLANS) ---

class PlanBase(BaseModel):
    code: str = Field(..., min_length=3, max_length=50, example="ENTERPRISE_2024")
    name: str = Field(..., min_length=3, max_length=100, example="Enterprise Plan")
    description: Optional[str] = Field(None)
    price_monthly: float = Field(..., ge=0)
    price_yearly: float = Field(..., ge=0)
    currency: str = Field("USD", min_length=3, max_length=3)
    limits: Dict[str, Any] = Field(default_factory=dict)
    features: Dict[str, bool] = Field(default_factory=dict)
    is_public: bool = Field(True)
    is_active: bool = Field(True)

    @field_validator('code')
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.isupper() or " " in v:
            raise ValueError("El código debe estar en mayúsculas y sin espacios.")
        return v

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_monthly: Optional[float] = Field(None, ge=0)
    price_yearly: Optional[float] = Field(None, ge=0)
    limits: Optional[Dict[str, Any]] = None
    features: Optional[Dict[str, bool]] = None
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None

class PlanRead(PlanBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    class Config: from_attributes = True

# --- TENANTS ---

class TenantBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    slug: str = Field(..., min_length=3, max_length=50)
    
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not v.islower() or " " in v:
            raise ValueError("El slug debe estar en minúsculas y sin espacios.")
        return v

class TenantCreate(BaseModel):
    name: str
    plan_id: uuid.UUID
    partner_id: Optional[uuid.UUID] = None
    admin_email: EmailStr
    admin_password: str

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

# --- SUBSCRIPTIONS ---

class SubscriptionUpdate(BaseModel):
    plan_id: Optional[uuid.UUID] = None
    status: Optional[SubscriptionStatus] = None
    current_period_end: Optional[datetime] = None

class SubscriptionRead(BaseModel):
    id: uuid.UUID
    plan: PlanRead # Anidar el plan completo
    status: SubscriptionStatus
    current_period_start: datetime
    current_period_end: datetime
    trial_end: Optional[datetime]
    class Config: from_attributes = True

class TenantRead(TenantBase):
    id: uuid.UUID
    partner_id: Optional[uuid.UUID]
    status: TenantStatus
    subscription: Optional[SubscriptionRead]
    class Config: from_attributes = True
