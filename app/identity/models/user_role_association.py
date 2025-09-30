# /app/identity/models/user_role_association.py
"""
Tabla de asociación para la relación muchos-a-muchos entre User y Role.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class UserRoleAssociation(Base):
    """Modelo de la tabla de asociación que vincula Usuarios con Roles."""
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
