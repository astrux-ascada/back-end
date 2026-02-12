import uuid
import enum
from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

# CORRECCIÓN: La Base declarativa se importa desde app.db.base_class
from app.db.base_class import Base

# --- Enums para Lógica de Negocio ---

class DiscountType(str, enum.Enum):
    PERCENTAGE = "percentage"       # Ej: 20% off
    FIXED_AMOUNT = "fixed_amount"   # Ej: $50 off

class CouponDuration(str, enum.Enum):
    ONCE = "once"             # Se aplica solo a la primera factura
    REPEATING = "repeating"   # Se aplica durante X meses
    FOREVER = "forever"       # Se aplica indefinidamente

class ReferralStatus(str, enum.Enum):
    PENDING = "pending"       # El invitado se registró pero no ha pagado
    CONVERTED = "converted"   # El invitado pagó su primera suscripción
    CANCELLED = "cancelled"   # El invitado canceló antes de pagar

# --- Modelos ---

class MarketingCampaign(Base):
    """
    Agrupa cupones para medir efectividad de estrategias (Ej: 'Black Friday 2024').
    """
    __tablename__ = "marketing_campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con cupones
    coupons = relationship("Coupon", back_populates="campaign")


class Coupon(Base):
    """
    El código de descuento real que se aplica.
    Soporta lógica compleja de duración (3, 6, 9 meses).
    """
    __tablename__ = "coupons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("marketing_campaigns.id"), nullable=True)
    
    code = Column(String(50), unique=True, nullable=False, index=True) # Ej: "VERANO2024"
    name = Column(String(100)) # Nombre interno para admins
    
    discount_type = Column(SQLAlchemyEnum(DiscountType), nullable=False)
    discount_value = Column(Float, nullable=False) # 20.0 (20%) o 50.0 ($50)
    
    # --- Lógica de Duración (Marketing) ---
    duration = Column(SQLAlchemyEnum(CouponDuration), default=CouponDuration.ONCE)
    duration_in_months = Column(Integer, nullable=True) # Solo si duration == REPEATING
    
    # --- Restricciones ---
    max_redemptions = Column(Integer, nullable=True) # Límite global de usos (ej: primeros 100)
    times_redeemed = Column(Integer, default=0)      # Contador de usos
    expires_at = Column(DateTime, nullable=True)     # Fecha límite para canjear
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("MarketingCampaign", back_populates="coupons")


class Referral(Base):
    """
    Rastrea quién invitó a quién.
    """
    __tablename__ = "referrals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # El Tenant que envió la invitación
    referrer_tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # El Tenant que fue invitado (se llena cuando se registran)
    referred_tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True, unique=True)
    
    # Código usado para el trackeo (puede ser el ID del referrer o un código especial)
    referral_code_used = Column(String(50), nullable=False)
    
    status = Column(SQLAlchemyEnum(ReferralStatus), default=ReferralStatus.PENDING)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    converted_at = Column(DateTime, nullable=True) # Fecha del primer pago

    # Relaciones (se definirán completamente al integrar con Tenant)
    # referrer = relationship("Tenant", foreign_keys=[referrer_tenant_id])
    # referee = relationship("Tenant", foreign_keys=[referred_tenant_id])
