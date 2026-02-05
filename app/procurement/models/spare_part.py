# /app/procurement/models/spare_part.py
"""
Modelo de la base de datos para la entidad SparePart (Repuesto).
"""
import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class SparePart(Base):
    """
    Representa un repuesto o consumible en el inventario.
    """
    __tablename__ = "spare_parts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    name = Column(String(100), nullable=False)
    part_number = Column(String(50), nullable=False, unique=True, index=True)
    stock_quantity = Column(Integer, default=0, nullable=False)
    price = Column(Float, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False) # Campo para soft delete

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relación inversa
    tenant = relationship("Tenant")
