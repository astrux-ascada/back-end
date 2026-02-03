# /app/identity/models/saas/plan.py
"""
Modelo para los Planes de Suscripción (Catálogo de Productos).
"""
import uuid
from sqlalchemy import Column, String, Float, JSON, Boolean, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Plan(Base):
    """
    Define un nivel de servicio comercial (ej: Starter, Pro, Enterprise).
    """
    __tablename__ = "plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identificación Comercial
    code = Column(String(50), unique=True, index=True, nullable=False, comment="Código inmutable del plan (ej: ENTERPRISE_2024)")
    name = Column(String(100), nullable=False, comment="Nombre comercial del plan")
    description = Column(String, nullable=True)
    
    # Precios (Base) - Los partners pueden tener listas de precios específicas, pero esto es la referencia global
    price_monthly = Column(Float, default=0.0, nullable=False)
    price_yearly = Column(Float, default=0.0, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Definición del Producto (JSONB para flexibilidad total)
    limits = Column(JSON, default={}, nullable=False, comment="Cuotas técnicas: {max_users: 10, max_assets: 100}")
    features = Column(JSON, default={}, nullable=False, comment="Flags de módulos: {module_procurement: true, isolation: 'SHARED'}")
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False, comment="Si es visible en la página de precios pública")

    # Relaciones
    subscriptions = relationship("Subscription", back_populates="plan")

    # Auditoría
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
