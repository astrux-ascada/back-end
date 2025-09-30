# /app/identity/models/permission.py
"""
Modelo de la base de datos para la entidad Permission.

Representa una acción atómica y específica que puede ser permitida o denegada,
formando la base del sistema de autorización granular (RBAC).
"""
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Permission(Base):
    """Modelo SQLAlchemy para un Permiso."""
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

    # --- Relación Inversa con Role ---
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
