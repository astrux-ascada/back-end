# /app/identity/models/role.py
"""
Modelo de la base de datos para la entidad Role.
"""
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Role(Base):
    """Modelo SQLAlchemy para un Rol del sistema."""
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

    # --- Relaciones Muchos-a-Muchos ---

    # Relación con User a través de la tabla user_roles
    users = relationship("User", secondary="user_roles", back_populates="roles")

    # Relación con Permission a través de la tabla role_permissions
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")
