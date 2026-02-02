# /app/identity/models/saas/subscription.py
"""
Modelo para las Suscripciones (Contratos) de los Clientes.
"""
import uuid
from sqlalchemy import Column, String, Boolean, JSON, TIMESTAMP, func, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base

class SubscriptionStatus(str, enum.Enum):
    TRIAL = "TRIAL"               # Periodo de prueba
    ACTIVE = "ACTIVE"             # Pagado y operativo
    PAST_DUE = "PAST_DUE"         # Impago (Bloqueo parcial)
    CANCELED = "CANCELED"         # Cancelado (Bloqueo total)
    EXPIRED = "EXPIRED"           # Fin de contrato

class Subscription(Base):
    """
    Vincula un Tenant con un Plan y define el estado de pago.
    """
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Relaciones
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), unique=True, nullable=False)
    tenant = relationship("Tenant", back_populates="subscription")
    
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"), nullable=False)
    plan = relationship("Plan", back_populates="subscriptions")
    
    # Estado del Contrato
    status = Column(String, default=SubscriptionStatus.TRIAL, nullable=False)
    
    # Fechas Críticas
    current_period_start = Column(TIMESTAMP(timezone=True), nullable=False)
    current_period_end = Column(TIMESTAMP(timezone=True), nullable=False, comment="Fecha de vencimiento/renovación")
    trial_end = Column(TIMESTAMP(timezone=True), nullable=True)
    canceled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # Configuración de Pago
    payment_method_id = Column(String, nullable=True, comment="ID del método de pago en Stripe/PayPal")
    billing_email = Column(String, nullable=True)
    
    # Auditoría
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
