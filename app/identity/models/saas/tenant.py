# /app/identity/models/saas/tenant.py
"""
Modelo para las Organizaciones (Clientes Finales) de Astruxa.
"""
import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    
    # --- Identidad y Branding ---
    logo_url = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    
    # --- Datos Fiscales y de Contacto ---
    tax_id = Column(String(50), nullable=True, comment="CIF, NIF, VAT ID")
    billing_address = Column(Text, nullable=True)
    contact_email = Column(String(100), nullable=True, comment="Email central para notificaciones del sistema")
    contact_phone = Column(String(50), nullable=True)

    # --- Configuración Regional y Operativa ---
    timezone = Column(String(50), default="UTC", nullable=False)
    language = Column(String(10), default="es", nullable=False)
    currency = Column(String(3), default="USD", nullable=False)

    # --- Estado y Borrado Lógico ---
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # --- Configuración Flexible ---
    config = Column(JSONB, nullable=True, default={})

    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"), nullable=True)
    partner = relationship("Partner", back_populates="tenants")
    
    subscription = relationship("Subscription", uselist=False, back_populates="tenant")
    users = relationship("User", back_populates="tenant")
