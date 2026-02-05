# /app/identity/models/role.py
"""
Modelo de la base de datos para la entidad Role.
"""
import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Role(Base):
    """Modelo SQLAlchemy para un Rol del sistema."""
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Aislamiento por Tenant (puede ser nulo para roles globales)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True, index=True)
    
    name = Column(String(50), nullable=False, index=True)
    description = Column(String(255), nullable=True)

    # --- Relaciones ---
    tenant = relationship("Tenant")

    # Relación con User a través de la tabla user_roles
    users = relationship("User", secondary="user_roles", back_populates="roles")

    # Relación con Permission a través de la tabla role_permissions
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")
