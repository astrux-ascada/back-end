# /app/identity/models/saas/tenant.py
"""
Modelo para las Organizaciones (Clientes Finales) de Astruxa.
"""
import uuid
from sqlalchemy import Column, String, Boolean, JSON, TIMESTAMP, func, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base

class TenantStatus(str, enum.Enum):
    PROVISIONING = "PROVISIONING" # Creando recursos (DB, Schemas)
    ACTIVE = "ACTIVE"             # Operativo
    SUSPENDED = "SUSPENDED"       # Bloqueado temporalmente (Admin decision)
    ARCHIVED = "ARCHIVED"         # Dado de baja (Soft delete)
    ERROR = "ERROR"               # Fallo en provisionamiento

class Tenant(Base):
    """
    Representa a una Organización Cliente (ej: Coca-Cola Planta Norte).
    """
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Relación con Partner (Quién vendió/gestiona este cliente)
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"), nullable=True, comment="Partner que gestiona este tenant. NULL = Directo Global")
    partner = relationship("Partner", back_populates="tenants")
    
    # Identificación
    name = Column(String(100), nullable=False, index=True)
    slug = Column(String(50), unique=True, index=True, nullable=False, comment="Identificador URL-friendly (ej: coca-cola-mx)")
    
    # Estado de Ciclo de Vida
    status = Column(String, default=TenantStatus.PROVISIONING, nullable=False)
    
    # Configuración de Aislamiento (Hybrid Multi-Tenancy)
    db_connection_string = Column(String, nullable=True, comment="Si NULL, usa DB compartida. Si tiene valor, usa DB dedicada.")
    
    # Configuración Visual y Técnica
    logo_url = Column(String, nullable=True)
    timezone = Column(String(50), default="UTC", nullable=False)
    locale = Column(String(10), default="es-ES", nullable=False)
    config = Column(JSON, default={}, nullable=False, comment="Configuración específica del tenant (colores, preferencias)")

    # Relaciones
    subscription = relationship("Subscription", uselist=False, back_populates="tenant")
    users = relationship("User", back_populates="tenant")

    # Auditoría
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
