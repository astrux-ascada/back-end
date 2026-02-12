# /app/identity/service_marketing.py
"""
Servicio de negocio para toda la lógica de Marketing: Campañas, Cupones y Referidos.
"""
import logging
import uuid
import random
import string
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ValidationException
from app.identity.models.saas.marketing import MarketingCampaign, Coupon, Referral, DiscountType, CouponDuration
from app.identity.models.saas.subscription import Subscription
from app.identity.models.saas.tenant import Tenant
from app.identity.schemas_saas import CampaignCreate, CampaignUpdate, CouponCreate, CouponUpdate

logger = logging.getLogger("app.identity.service_marketing")

class MarketingService:
    def __init__(self, db: Session):
        self.db = db

    # --- Gestión de Campañas ---

    def create_campaign(self, campaign_in: CampaignCreate) -> MarketingCampaign:
        logger.info(f"Creando nueva campaña de marketing: {campaign_in.name}")
        campaign = MarketingCampaign(**campaign_in.model_dump())
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def list_campaigns(self) -> List[MarketingCampaign]:
        return self.db.query(MarketingCampaign).all()

    # --- Gestión de Cupones ---

    def create_coupon(self, coupon_in: CouponCreate) -> Coupon:
        logger.info(f"Creando nuevo cupón con código: {coupon_in.code}")
        
        # Validación de lógica de negocio
        if coupon_in.duration == CouponDuration.REPEATING and not coupon_in.duration_in_months:
            raise ValidationException("Para cupones de tipo 'REPEATING', se requiere 'duration_in_months'.")
        
        coupon = Coupon(**coupon_in.model_dump())
        self.db.add(coupon)
        self.db.commit()
        self.db.refresh(coupon)
        return coupon

    def list_coupons(self) -> List[Coupon]:
        return self.db.query(Coupon).all()

    def validate_coupon(self, code: str) -> Coupon:
        """
        Valida si un cupón es aplicable.
        Lanza excepciones si no lo es.
        """
        coupon = self.db.query(Coupon).filter(Coupon.code.ilike(code)).first()

        if not coupon:
            raise NotFoundException("El cupón no existe.")
        if not coupon.is_active:
            raise ValidationException("El cupón ya no está activo.")
        if coupon.expires_at and coupon.expires_at < datetime.utcnow():
            raise ValidationException("El cupón ha expirado.")
        if coupon.max_redemptions and coupon.times_redeemed >= coupon.max_redemptions:
            raise ValidationException("Este cupón ha alcanzado su límite de usos.")
            
        return coupon

    def apply_coupon_to_subscription(self, tenant_id: uuid.UUID, code: str) -> Subscription:
        """
        Aplica un cupón a la suscripción de un tenant.
        """
        logger.info(f"Intentando aplicar cupón '{code}' al tenant {tenant_id}")
        
        coupon = self.validate_coupon(code)
        
        subscription = self.db.query(Subscription).filter(Subscription.tenant_id == tenant_id).first()
        if not subscription:
            raise NotFoundException("No se encontró una suscripción para este tenant.")
        if subscription.applied_coupon_id:
            raise ValidationException("Ya hay un cupón aplicado a esta suscripción.")

        # Calcular precio final
        plan_price = subscription.plan.price_monthly # Asumimos mensual por simplicidad
        final_price = plan_price

        if coupon.discount_type == DiscountType.PERCENTAGE:
            discount = (plan_price * coupon.discount_value) / 100
            final_price = max(0, plan_price - discount)
        elif coupon.discount_type == DiscountType.FIXED_AMOUNT:
            final_price = max(0, plan_price - coupon.discount_value)

        # Aplicar cupón
        subscription.applied_coupon_id = coupon.id
        subscription.final_price = final_price
        coupon.times_redeemed += 1
        
        self.db.add(subscription)
        self.db.add(coupon)
        self.db.commit()
        
        logger.info(f"Cupón '{code}' aplicado exitosamente al tenant {tenant_id}. Nuevo precio: {final_price}")
        
        # Aquí se podría emitir un evento para auditoría
        # event_broker.publish("marketing.coupon.applied", {"tenant_id": tenant_id, "coupon_code": code})
        
        self.db.refresh(subscription)
        return subscription

    # --- Gestión de Referidos ---

    def generate_referral_code(self, tenant: Tenant) -> str:
        """
        Genera un código de referido único para un tenant y lo guarda.
        """
        if tenant.referral_code:
            return tenant.referral_code
            
        # Generar un código aleatorio y verificar que no exista
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not self.db.query(Tenant).filter(Tenant.referral_code == code).first():
                tenant.referral_code = code
                self.db.add(tenant)
                self.db.commit()
                logger.info(f"Código de referido '{code}' generado para el tenant {tenant.id}")
                return code
