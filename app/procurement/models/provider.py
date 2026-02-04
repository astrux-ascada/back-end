# /app/procurement/models/provider.py
"""
Modelo de la base de datos para la entidad Provider.
"""
import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Provider(Base):
    """
    Representa a un proveedor de servicios o repuestos.
    """
    __tablename__ = "providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    name = Column(String(100), nullable=False, index=True)
    contact_info = Column(String(255), nullable=True)
    specialty = Column(String(100), nullable=True)
    performance_score = Column(Float, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False) # Campo para soft delete

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relación inversa
    tenant = relationship("Tenant")
