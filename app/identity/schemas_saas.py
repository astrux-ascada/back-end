# /app/identity/schemas_saas.py
"""
Esquemas Pydantic para la gestión del modelo de negocio SaaS, incluyendo marketing.
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, EmailStr

from app.identity.models.saas.marketing import DiscountType, CouponDuration

# --- Esquemas para MarketingCampaign ---

class CampaignBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class CampaignRead(CampaignBase):
    id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True

# --- Esquemas para Coupon ---

class CouponBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: Optional[str] = Field(None, max_length=100)
    campaign_id: Optional[uuid.UUID] = None
    discount_type: DiscountType
    discount_value: float
    duration: CouponDuration = CouponDuration.ONCE
    duration_in_months: Optional[int] = None
    max_redemptions: Optional[int] = None
    expires_at: Optional[datetime] = None
    is_active: bool = True

class CouponCreate(CouponBase):
    pass

class CouponUpdate(BaseModel):
    name: Optional[str] = None
    campaign_id: Optional[uuid.UUID] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class CouponRead(CouponBase):
    id: uuid.UUID
    times_redeemed: int
    created_at: datetime
    class Config:
        from_attributes = True

class ApplyCouponRequest(BaseModel):
    coupon_code: str = Field(..., description="El código del cupón a aplicar.")

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
    # ... (resto de campos de Tenant)

# ... (resto de esquemas de Tenant, Suscripción, etc.)
