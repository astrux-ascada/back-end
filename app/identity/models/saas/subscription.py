# /app/identity/models/saas/subscription.py
"""
Modelo para las Suscripciones (Contratos) de los Clientes.
"""
import uuid
import enum
from sqlalchemy import Column, String, TIMESTAMP, func, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PAST_DUE = "PAST_DUE"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), unique=True, nullable=False)
    tenant = relationship("Tenant", back_populates="subscription")
    
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"), nullable=False)
    plan = relationship("Plan", back_populates="subscriptions")
    
    status = Column(Enum(SubscriptionStatus), nullable=False)
    
    current_period_start = Column(TIMESTAMP(timezone=True), nullable=True)
    current_period_end = Column(TIMESTAMP(timezone=True), nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
