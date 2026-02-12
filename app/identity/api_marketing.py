# /app/identity/api_marketing.py
"""
API Routers para la gestión de Campañas, Cupones y Referidos.
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status # <-- Importaciones añadidas

from app.dependencies.auth import get_current_active_user
from app.dependencies.permissions import require_permission
from app.dependencies.services import get_marketing_service
from app.identity.models import User
from app.identity.service_marketing import MarketingService
from app.identity.schemas_saas import (
    CampaignCreate, CampaignUpdate, CampaignRead,
    CouponCreate, CouponUpdate, CouponRead,
    ApplyCouponRequest
)
from app.identity.schemas import UserRead

logger = logging.getLogger("app.identity.api_marketing")

# --- Router para Administradores de Plataforma ---
# Se montará bajo /api/v1/sys-mgt/marketing
admin_router = APIRouter(prefix="/marketing", tags=["Admin - Marketing"])

# --- Endpoints para Campañas ---

@admin_router.post("/campaigns", response_model=CampaignRead, dependencies=[Depends(require_permission("campaign:create"))])
def create_campaign(campaign_in: CampaignCreate, service: MarketingService = Depends(get_marketing_service)):
    return service.create_campaign(campaign_in)

@admin_router.get("/campaigns", response_model=List[CampaignRead], dependencies=[Depends(require_permission("campaign:read"))])
def list_campaigns(service: MarketingService = Depends(get_marketing_service)):
    return service.list_campaigns()

# --- Endpoints para Cupones ---

@admin_router.post("/coupons", response_model=CouponRead, dependencies=[Depends(require_permission("coupon:create"))])
def create_coupon(coupon_in: CouponCreate, service: MarketingService = Depends(get_marketing_service)):
    return service.create_coupon(coupon_in)

@admin_router.get("/coupons", response_model=List[CouponRead], dependencies=[Depends(require_permission("coupon:read"))])
def list_coupons(service: MarketingService = Depends(get_marketing_service)):
    return service.list_coupons()


# --- Router para Clientes (Tenants) ---
# Se montará en otro lugar, ej: bajo /api/v1/saas/
client_router = APIRouter(tags=["SaaS - Self-Service"])

@client_router.post("/me/subscription/apply-coupon", dependencies=[Depends(require_permission("coupon:apply"))])
def apply_coupon(
    request: ApplyCouponRequest,
    current_user: User = Depends(get_current_active_user),
    service: MarketingService = Depends(get_marketing_service)
):
    """Aplica un cupón a la suscripción del tenant del usuario actual."""
    if not current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta acción solo es válida para usuarios de un tenant.")
    
    service.apply_coupon_to_subscription(current_user.tenant_id, request.coupon_code)
    return {"message": "Cupón aplicado exitosamente."}

@client_router.get("/me/referral-code", response_model=dict)
def get_my_referral_code(
    current_user: User = Depends(get_current_active_user),
    service: MarketingService = Depends(get_marketing_service)
):
    """Obtiene el código de referido para el tenant del usuario actual."""
    if not current_user.tenant:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta acción solo es válida para usuarios de un tenant.")
        
    code = service.generate_referral_code(current_user.tenant)
    return {"referral_code": code}
