# /app/identity/models/role_permission_association.py
"""
Tabla de asociación para la relación muchos-a-muchos entre Role y Permission.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class RolePermissionAssociation(Base):
    """Modelo de la tabla de asociación que vincula Roles con Permisos."""
    __tablename__ = "role_permissions"

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"), primary_key=True)
