# /app/procurement/models/spare_part.py
"""
Modelo de la base de datos para la entidad SparePart (Repuesto).
"""
import uuid
from sqlalchemy import Column, String, Float, Integer, ForeignKey, func, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class SparePart(Base):
    """Modelo SQLAlchemy para un Repuesto o Parte."""
    __tablename__ = "spare_parts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    part_number = Column(String(100), nullable=True, index=True, comment="Manufacturer Part Number")
    
    # --- Inventario ---
    current_stock = Column(Integer, default=0, nullable=False)
    min_stock_level = Column(Integer, default=0, nullable=False, comment="Threshold for reordering")
    unit_cost = Column(Float, default=0.0, nullable=False)
    
    # --- Relaciones ---
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=True)
    provider = relationship("Provider", back_populates="spare_parts")
    
    is_active = Column(Boolean, default=True, nullable=False)

    # --- Auditoría ---
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
