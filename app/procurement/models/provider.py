# /app/procurement/models/provider.py
"""
Modelo de la base de datos para la entidad Provider.

Representa un proveedor externo, contratista o vendedor.
"""
import uuid

from sqlalchemy import Column, String, Float, func, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Provider(Base):
    """Modelo SQLAlchemy para un Proveedor."""
    __tablename__ = "providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(100), unique=True, index=True, nullable=False)
    contact_info = Column(String(255), nullable=True, comment="Email, phone, or address of the provider.")
    specialty = Column(String(100), index=True, nullable=True, comment="Area of expertise, e.g., Robotics, HVAC, PLC Programming.")
    
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    performance_score = Column(Float, nullable=True, index=True, comment="A score from 0-100 representing provider performance.")

    # --- Relación Inversa ---
    spare_parts = relationship("SparePart", back_populates="provider")

    # --- Campos de Auditoría ---
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
