
import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.db.base import Base

# Tabla de asociación para la relación muchos a muchos entre User y Section
user_sections = Table(
    "user_sections",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("section_id", UUID(as_uuid=True), ForeignKey("sections.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)

    # --- Relationships ---
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- Foreign Keys ---
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))

    # --- Relationships ---
    role = relationship("Role", back_populates="users")
    maintenance_orders = relationship("MaintenanceOrder", back_populates="assigned_to")

    # Relación con las secciones (muchos a muchos)
    sections = relationship(
        "Section", secondary=user_sections, back_populates="users"
    )
