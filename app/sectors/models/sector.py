# /app/sectors/models/sector.py
"""
Modelo de la base de datos para la entidad Sector.
"""
import uuid
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Sector(Base):
    """Modelo SQLAlchemy para un Sector de la planta."""
    __tablename__ = "sectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Aislamiento por Tenant
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    
    # Jerarquía
    parent_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id"), nullable=True)
    
    # Soft Delete
    is_active = Column(Boolean, default=True, nullable=False)

    # Relaciones
    parent = relationship("Sector", remote_side=[id], backref="children")
    
    # Las relaciones `users` y `assets` se definen externamente o con back_populates si los modelos están disponibles
