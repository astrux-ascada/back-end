# /app/identity/models/saas/plan.py
"""
Modelo para los Planes de Suscripción (Catálogo de Productos).
"""
import uuid
from sqlalchemy import Column, String, Float, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    price_monthly = Column(Float, nullable=False)
    price_yearly = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    limits = Column(JSON, nullable=True)
    features = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    subscriptions = relationship("Subscription", back_populates="plan")
