# /app/identity/models/saas/partner.py
"""
Modelo para los Operadores Regionales (Partners) de Astruxa.
"""
import uuid
from sqlalchemy import Column, String, Boolean, Float, JSON, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Partner(Base):
    """
    Representa a un Operador Regional o Revendedor de Astruxa.
    Ej: Astruxa México, Astruxa España.
    """
    __tablename__ = "partners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identificación
    code = Column(String(50), unique=True, index=True, nullable=False, comment="Código único del partner (ej: ASTRUXA_MX)")
    name = Column(String(100), nullable=False, comment="Nombre legal del partner")
    
    # Configuración Regional
    region = Column(String(50), nullable=False, comment="Región operativa (ej: LATAM, EMEA)")
    currency = Column(String(3), default="USD", nullable=False, comment="Moneda base para facturación (ISO 4217)")
    tax_id = Column(String(50), nullable=True, comment="Identificación fiscal del partner")
    
    # Negocio
    commission_rate = Column(Float, default=0.0, nullable=False, comment="Porcentaje de comisión sobre ventas")
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Configuración Técnica
    config = Column(JSON, default={}, nullable=False, comment="Configuración específica del partner (logos, soporte, etc)")

    # Relaciones
    tenants = relationship("Tenant", back_populates="partner")

    # Auditoría
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
