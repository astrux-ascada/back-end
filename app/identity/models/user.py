# /app/identity/models/user.py
"""
Modelo de la base de datos para la entidad User.
"""
import uuid

from sqlalchemy import Boolean, Column, String, func, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    """Modelo SQLAlchemy para un Usuario del sistema."""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # --- Relación con Role ---
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=True)
    role = relationship("Role", back_populates="users")

    # --- Campos de Perfil y Autenticación ---
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String(60), nullable=True)
    username = Column(String(25), unique=True, nullable=True)
    phone = Column(String(25), nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True, nullable=False)
    position = Column(String(100), nullable=True)
    occupation = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    preferred_language = Column(String(10), default="es", nullable=False)
    employee_id = Column(String(50), unique=True, nullable=True)

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
