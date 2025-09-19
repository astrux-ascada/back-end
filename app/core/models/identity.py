
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from app.core.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)

    # --- Relationships ---
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- Foreign Keys ---
    role_id = Column(Integer, ForeignKey("roles.id"))

    # --- Relationships ---
    role = relationship("Role", back_populates="users")
    maintenance_orders = relationship("MaintenanceOrder", back_populates="assigned_to")
